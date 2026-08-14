#!/usr/bin/env python3
"""
qq_lyrics.py
------------
Fetch word-by-word synced lyrics (QRC format) from QQ Music (y.qq.com)
given a song name and artist.

How it works:
1. Search QQ Music via the unified gateway (u.y.qq.com/cgi-bin/musicu.fcg)
   to find the songmid/songid matching the query.
2. Request the QRC (word-by-word karaoke) lyric blob for that song.
3. QQ Music returns the QRC payload obfuscated: it's hex-encoded bytes that
   are DES-encrypted (ECB, in 3 rounds: decrypt->encrypt->decrypt with 3
   fixed keys) then zlib-compressed.

   IMPORTANT: QQ Music's client does NOT use standard/correct DES. Its
   QQMusicCommon.dll links a copy of Brad Conte's public-domain DES
   implementation that has a well-known transcription bug in sbox4 (a
   duplicated "10" where the real DES spec has a "1"). Because that buggy
   S-box is what was actually used to encrypt the lyric blobs server-side,
   a *standard-compliant* DES implementation (like pycryptodome's) will
   never invert it correctly - it'll silently produce garbage that fails
   the zlib decompress step every time, which is exactly the
   "incorrect header check" error from the debug log/screenshot.

   The fix: reproduce QQ's DES bug-for-bug. This script embeds the exact
   des.c (buggy sbox4 and all - this is the same file used by the
   wangqr/QQMusicDES project, a drop-in replacement for
   QQMusicCommon.dll), compiles it once into a small shared library, and
   calls it via ctypes instead of using pycryptodome.
4. Falls back to the plain LRC endpoint if QRC isn't available/decodable.

Note on voice/duet tags: QRC does NOT carry v1/v2/bg (vadata -
that's an Apple Music TTML (ttm:agent / ttm:role="x-bg") and Lyricifyoice-role) met
(.lys/.lqe) concept, not a QQ Music one. If your pipeline needs duet or
background-vocal tagging, that has to come from a TTML or Lyricify source
for the same track, not from this QRC fetch - treat this as your plain
"word-by-word timing" tier, not a voice-tag source.

Speed: the DES decrypt + zlib inflate is local compute and takes well
under a millisecond - it is never the bottleneck. The ~2 HTTP round-trips
to y.qq.com (search + QRC fetch) dominate the time. Run with debug=True
(or answer 'y' at the debug prompt) to see a per-phase timing breakdown
and confirm whether the DES library is being recompiled every run (it
should only compile once - subsequent runs from the same script directory
reuse the cached .so/.dylib/.dll in .qq_des_cache/).

Requirements:
    pip install requests --break-system-packages
    A C compiler (gcc/clang) available on PATH - used once to build the
    bundled DES implementation into a cached .so/.dylib/.dll next to this
    script. No third-party crypto library is needed anymore.

Usage:
    python qq_lyrics.py
    (then follow the prompts for song name / artist)
"""

import ctypes
import os
import re
import subprocess
import sys
import tempfile
import time
import zlib
import json
import binascii
import platform

import requests


HEADERS = {
    "Referer": "https://y.qq.com/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}

SEARCH_URL = "https://u.y.qq.com/cgi-bin/musicu.fcg"
QRC_URL = "https://c.y.qq.com/qqmusic/fcgi-bin/lyric_download.fcg"
LYRIC_FALLBACK_URL = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"

QRC_KEY1 = b"!@#)(NHL"   # first 8 bytes of "!@#)(NHLiuy*$%^&"
QRC_KEY2 = b"123ZXC!@"   # first 8 bytes of "123ZXC!@#)(*$%^&"
QRC_KEY3 = b"!@#)(*$%"   # first 8 bytes of "!@#)(*$%^&abcDEF"

# Reused across calls so repeated lookups (e.g. from a long-running app
# that queries many songs) get TCP/TLS connection keep-alive instead of
# paying a fresh handshake to y.qq.com every time. Network round-trips are
# almost always the dominant cost here, not the DES/zlib decode step.
_SESSION = requests.Session()
_SESSION.headers.update(HEADERS)


# --------------------------------------------------------------------------
# Bug-for-bug faithful DES (QQ Music's actual algorithm), built from des.c
# --------------------------------------------------------------------------

_DES_H_SRC = r"""
#ifndef DES_H
#define DES_H
#include <stddef.h>
#define DES_BLOCK_SIZE 8
typedef unsigned char BYTE;
typedef unsigned int WORD;
typedef enum { DES_ENCRYPT, DES_DECRYPT } DES_MODE;
void des_key_setup(const BYTE key[], BYTE schedule[][6], DES_MODE mode);
void des_crypt(const BYTE in[], BYTE out[], const BYTE key[][6]);
void three_des_key_setup(const BYTE key[], BYTE schedule[][16][6], DES_MODE mode);
void three_des_crypt(const BYTE in[], BYTE out[], const BYTE key[][16][6]);
#endif
"""

# This is QQ Music's actual (buggy) DES - reproduced verbatim, including the
# duplicated "10" in sbox4 (row 4) that real DES does not have. Do not "fix"
# that S-box; the bug is exactly what makes this decrypt QQ's lyric blobs.
_DES_C_SRC = r"""
#include <stdlib.h>
#include <memory.h>
#include "des.h"

#define BITNUM(a,b,c) (((a[(b)/32*4+3-(b)%32/8] >> (7 - (b%8))) & 0x01) << (c))
#define BITNUMINTR(a,b,c) ((((a) >> (31 - (b))) & 0x00000001) << (c))
#define BITNUMINTL(a,b,c) ((((a) << (b)) & 0x80000000) >> (c))
#define SBOXBIT(a) (((a) & 0x20) | (((a) & 0x1f) >> 1) | (((a) & 0x01) << 4))

static const BYTE sbox1[64] = {
	14,  4,  13,  1,   2, 15,  11,  8,   3, 10,   6, 12,   5,  9,   0,  7,
	 0, 15,   7,  4,  14,  2,  13,  1,  10,  6,  12, 11,   9,  5,   3,  8,
	 4,  1,  14,  8,  13,  6,   2, 11,  15, 12,   9,  7,   3, 10,   5,  0,
	15, 12,   8,  2,   4,  9,   1,  7,   5, 11,   3, 14,  10,  0,   6, 13
};
static const BYTE sbox2[64] = {
	15,  1,   8, 14,   6, 11,   3,  4,   9,  7,   2, 13,  12,  0,   5, 10,
	 3, 13,   4,  7,  15,  2,   8, 15,  12,  0,   1, 10,   6,  9,  11,  5,
	 0, 14,   7, 11,  10,  4,  13,  1,   5,  8,  12,  6,   9,  3,   2, 15,
	13,  8,  10,  1,   3, 15,   4,  2,  11,  6,   7, 12,   0,  5,  14,  9
};
static const BYTE sbox3[64] = {
	10,  0,   9, 14,   6,  3,  15,  5,   1, 13,  12,  7,  11,  4,   2,  8,
	13,  7,   0,  9,   3,  4,   6, 10,   2,  8,   5, 14,  12, 11,  15,  1,
	13,  6,   4,  9,   8, 15,   3,  0,  11,  1,   2, 12,   5, 10,  14,  7,
	 1, 10,  13,  0,   6,  9,   8,  7,   4, 15,  14,  3,  11,  5,   2, 12
};
static const BYTE sbox4[64] = {
	 7, 13,  14,  3,   0,  6,   9, 10,   1,  2,   8,  5,  11, 12,   4, 15,
	13,  8,  11,  5,   6, 15,   0,  3,   4,  7,   2, 12,   1, 10,  14,  9,
	10,  6,   9,  0,  12, 11,   7, 13,  15,  1,   3, 14,   5,  2,   8,  4,
	 3, 15,   0,  6,  10, 10,  13,  8,   9,  4,   5, 11,  12,  7,   2, 14
};
static const BYTE sbox5[64] = {
	 2, 12,   4,  1,   7, 10,  11,  6,   8,  5,   3, 15,  13,  0,  14,  9,
	14, 11,   2, 12,   4,  7,  13,  1,   5,  0,  15, 10,   3,  9,   8,  6,
	 4,  2,   1, 11,  10, 13,   7,  8,  15,  9,  12,  5,   6,  3,   0, 14,
	11,  8,  12,  7,   1, 14,   2, 13,   6, 15,   0,  9,  10,  4,   5,  3
};
static const BYTE sbox6[64] = {
	12,  1,  10, 15,   9,  2,   6,  8,   0, 13,   3,  4,  14,  7,   5, 11,
	10, 15,   4,  2,   7, 12,   9,  5,   6,  1,  13, 14,   0, 11,   3,  8,
	 9, 14,  15,  5,   2,  8,  12,  3,   7,  0,   4, 10,   1, 13,  11,  6,
	 4,  3,   2, 12,   9,  5,  15, 10,  11, 14,   1,  7,   6,  0,   8, 13
};
static const BYTE sbox7[64] = {
	 4, 11,   2, 14,  15,  0,   8, 13,   3, 12,   9,  7,   5, 10,   6,  1,
	13,  0,  11,  7,   4,  9,   1, 10,  14,  3,   5, 12,   2, 15,   8,  6,
	 1,  4,  11, 13,  12,  3,   7, 14,  10, 15,   6,  8,   0,  5,   9,  2,
	 6, 11,  13,  8,   1,  4,  10,  7,   9,  5,   0, 15,  14,  2,   3, 12
};
static const BYTE sbox8[64] = {
	13,  2,   8,  4,   6, 15,  11,  1,  10,  9,   3, 14,   5,  0,  12,  7,
	 1, 15,  13,  8,  10,  3,   7,  4,  12,  5,   6, 11,   0, 14,   9,  2,
	 7, 11,   4,  1,   9, 12,  14,  2,   0,  6,  10, 13,  15,  3,   5,  8,
	 2,  1,  14,  7,   4, 10,   8, 13,  15, 12,   9,  0,   3,  5,   6, 11
};

void IP(WORD state[], const BYTE in[])
{
	state[0] = BITNUM(in,57,31) | BITNUM(in,49,30) | BITNUM(in,41,29) | BITNUM(in,33,28) |
				  BITNUM(in,25,27) | BITNUM(in,17,26) | BITNUM(in,9,25) | BITNUM(in,1,24) |
				  BITNUM(in,59,23) | BITNUM(in,51,22) | BITNUM(in,43,21) | BITNUM(in,35,20) |
				  BITNUM(in,27,19) | BITNUM(in,19,18) | BITNUM(in,11,17) | BITNUM(in,3,16) |
				  BITNUM(in,61,15) | BITNUM(in,53,14) | BITNUM(in,45,13) | BITNUM(in,37,12) |
				  BITNUM(in,29,11) | BITNUM(in,21,10) | BITNUM(in,13,9) | BITNUM(in,5,8) |
				  BITNUM(in,63,7) | BITNUM(in,55,6) | BITNUM(in,47,5) | BITNUM(in,39,4) |
				  BITNUM(in,31,3) | BITNUM(in,23,2) | BITNUM(in,15,1) | BITNUM(in,7,0);

	state[1] = BITNUM(in,56,31) | BITNUM(in,48,30) | BITNUM(in,40,29) | BITNUM(in,32,28) |
				  BITNUM(in,24,27) | BITNUM(in,16,26) | BITNUM(in,8,25) | BITNUM(in,0,24) |
				  BITNUM(in,58,23) | BITNUM(in,50,22) | BITNUM(in,42,21) | BITNUM(in,34,20) |
				  BITNUM(in,26,19) | BITNUM(in,18,18) | BITNUM(in,10,17) | BITNUM(in,2,16) |
				  BITNUM(in,60,15) | BITNUM(in,52,14) | BITNUM(in,44,13) | BITNUM(in,36,12) |
				  BITNUM(in,28,11) | BITNUM(in,20,10) | BITNUM(in,12,9) | BITNUM(in,4,8) |
				  BITNUM(in,62,7) | BITNUM(in,54,6) | BITNUM(in,46,5) | BITNUM(in,38,4) |
				  BITNUM(in,30,3) | BITNUM(in,22,2) | BITNUM(in,14,1) | BITNUM(in,6,0);
}

void InvIP(WORD state[], BYTE in[])
{
	in[3] = BITNUMINTR(state[1],7,7) | BITNUMINTR(state[0],7,6) | BITNUMINTR(state[1],15,5) |
			  BITNUMINTR(state[0],15,4) | BITNUMINTR(state[1],23,3) | BITNUMINTR(state[0],23,2) |
			  BITNUMINTR(state[1],31,1) | BITNUMINTR(state[0],31,0);

	in[2] = BITNUMINTR(state[1],6,7) | BITNUMINTR(state[0],6,6) | BITNUMINTR(state[1],14,5) |
			  BITNUMINTR(state[0],14,4) | BITNUMINTR(state[1],22,3) | BITNUMINTR(state[0],22,2) |
			  BITNUMINTR(state[1],30,1) | BITNUMINTR(state[0],30,0);

	in[1] = BITNUMINTR(state[1],5,7) | BITNUMINTR(state[0],5,6) | BITNUMINTR(state[1],13,5) |
			  BITNUMINTR(state[0],13,4) | BITNUMINTR(state[1],21,3) | BITNUMINTR(state[0],21,2) |
			  BITNUMINTR(state[1],29,1) | BITNUMINTR(state[0],29,0);

	in[0] = BITNUMINTR(state[1],4,7) | BITNUMINTR(state[0],4,6) | BITNUMINTR(state[1],12,5) |
			  BITNUMINTR(state[0],12,4) | BITNUMINTR(state[1],20,3) | BITNUMINTR(state[0],20,2) |
			  BITNUMINTR(state[1],28,1) | BITNUMINTR(state[0],28,0);

	in[7] = BITNUMINTR(state[1],3,7) | BITNUMINTR(state[0],3,6) | BITNUMINTR(state[1],11,5) |
			  BITNUMINTR(state[0],11,4) | BITNUMINTR(state[1],19,3) | BITNUMINTR(state[0],19,2) |
			  BITNUMINTR(state[1],27,1) | BITNUMINTR(state[0],27,0);

	in[6] = BITNUMINTR(state[1],2,7) | BITNUMINTR(state[0],2,6) | BITNUMINTR(state[1],10,5) |
			  BITNUMINTR(state[0],10,4) | BITNUMINTR(state[1],18,3) | BITNUMINTR(state[0],18,2) |
			  BITNUMINTR(state[1],26,1) | BITNUMINTR(state[0],26,0);

	in[5] = BITNUMINTR(state[1],1,7) | BITNUMINTR(state[0],1,6) | BITNUMINTR(state[1],9,5) |
			  BITNUMINTR(state[0],9,4) | BITNUMINTR(state[1],17,3) | BITNUMINTR(state[0],17,2) |
			  BITNUMINTR(state[1],25,1) | BITNUMINTR(state[0],25,0);

	in[4] = BITNUMINTR(state[1],0,7) | BITNUMINTR(state[0],0,6) | BITNUMINTR(state[1],8,5) |
			  BITNUMINTR(state[0],8,4) | BITNUMINTR(state[1],16,3) | BITNUMINTR(state[0],16,2) |
			  BITNUMINTR(state[1],24,1) | BITNUMINTR(state[0],24,0);
}

WORD f(WORD state, const BYTE key[])
{
	BYTE lrgstate[6];
	WORD t1,t2;

	t1 = BITNUMINTL(state,31,0) | ((state & 0xf0000000) >> 1) | BITNUMINTL(state,4,5) |
		  BITNUMINTL(state,3,6) | ((state & 0x0f000000) >> 3) | BITNUMINTL(state,8,11) |
		  BITNUMINTL(state,7,12) | ((state & 0x00f00000) >> 5) | BITNUMINTL(state,12,17) |
		  BITNUMINTL(state,11,18) | ((state & 0x000f0000) >> 7) | BITNUMINTL(state,16,23);

	t2 = BITNUMINTL(state,15,0) | ((state & 0x0000f000) << 15) | BITNUMINTL(state,20,5) |
		  BITNUMINTL(state,19,6) | ((state & 0x00000f00) << 13) | BITNUMINTL(state,24,11) |
		  BITNUMINTL(state,23,12) | ((state & 0x000000f0) << 11) | BITNUMINTL(state,28,17) |
		  BITNUMINTL(state,27,18) | ((state & 0x0000000f) << 9) | BITNUMINTL(state,0,23);

	lrgstate[0] = (t1 >> 24) & 0x000000ff;
	lrgstate[1] = (t1 >> 16) & 0x000000ff;
	lrgstate[2] = (t1 >> 8) & 0x000000ff;
	lrgstate[3] = (t2 >> 24) & 0x000000ff;
	lrgstate[4] = (t2 >> 16) & 0x000000ff;
	lrgstate[5] = (t2 >> 8) & 0x000000ff;

	lrgstate[0] ^= key[0];
	lrgstate[1] ^= key[1];
	lrgstate[2] ^= key[2];
	lrgstate[3] ^= key[3];
	lrgstate[4] ^= key[4];
	lrgstate[5] ^= key[5];

	state = (sbox1[SBOXBIT(lrgstate[0] >> 2)] << 28) |
			  (sbox2[SBOXBIT(((lrgstate[0] & 0x03) << 4) | (lrgstate[1] >> 4))] << 24) |
			  (sbox3[SBOXBIT(((lrgstate[1] & 0x0f) << 2) | (lrgstate[2] >> 6))] << 20) |
			  (sbox4[SBOXBIT(lrgstate[2] & 0x3f)] << 16) |
			  (sbox5[SBOXBIT(lrgstate[3] >> 2)] << 12) |
			  (sbox6[SBOXBIT(((lrgstate[3] & 0x03) << 4) | (lrgstate[4] >> 4))] << 8) |
			  (sbox7[SBOXBIT(((lrgstate[4] & 0x0f) << 2) | (lrgstate[5] >> 6))] << 4) |
				sbox8[SBOXBIT(lrgstate[5] & 0x3f)];

	state = BITNUMINTL(state,15,0) | BITNUMINTL(state,6,1) | BITNUMINTL(state,19,2) |
			  BITNUMINTL(state,20,3) | BITNUMINTL(state,28,4) | BITNUMINTL(state,11,5) |
			  BITNUMINTL(state,27,6) | BITNUMINTL(state,16,7) | BITNUMINTL(state,0,8) |
			  BITNUMINTL(state,14,9) | BITNUMINTL(state,22,10) | BITNUMINTL(state,25,11) |
			  BITNUMINTL(state,4,12) | BITNUMINTL(state,17,13) | BITNUMINTL(state,30,14) |
			  BITNUMINTL(state,9,15) | BITNUMINTL(state,1,16) | BITNUMINTL(state,7,17) |
			  BITNUMINTL(state,23,18) | BITNUMINTL(state,13,19) | BITNUMINTL(state,31,20) |
			  BITNUMINTL(state,26,21) | BITNUMINTL(state,2,22) | BITNUMINTL(state,8,23) |
			  BITNUMINTL(state,18,24) | BITNUMINTL(state,12,25) | BITNUMINTL(state,29,26) |
			  BITNUMINTL(state,5,27) | BITNUMINTL(state,21,28) | BITNUMINTL(state,10,29) |
			  BITNUMINTL(state,3,30) | BITNUMINTL(state,24,31);

	return(state);
}

void des_key_setup(const BYTE key[], BYTE schedule[][6], DES_MODE mode)
{
	WORD i, j, to_gen, C, D;
	const WORD key_rnd_shift[16] = {1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1};
	const WORD key_perm_c[28] = {56,48,40,32,24,16,8,0,57,49,41,33,25,17,
	                             9,1,58,50,42,34,26,18,10,2,59,51,43,35};
	const WORD key_perm_d[28] = {62,54,46,38,30,22,14,6,61,53,45,37,29,21,
	                             13,5,60,52,44,36,28,20,12,4,27,19,11,3};
	const WORD key_compression[48] = {13,16,10,23,0,4,2,27,14,5,20,9,
	                                  22,18,11,3,25,7,15,6,26,19,12,1,
	                                  40,51,30,36,46,54,29,39,50,44,32,47,
	                                  43,48,38,55,33,52,45,41,49,35,28,31};

	for (i = 0, j = 31, C = 0; i < 28; ++i, --j)
		C |= BITNUM(key,key_perm_c[i],j);
	for (i = 0, j = 31, D = 0; i < 28; ++i, --j)
		D |= BITNUM(key,key_perm_d[i],j);

	for (i = 0; i < 16; ++i) {
		C = ((C << key_rnd_shift[i]) | (C >> (28-key_rnd_shift[i]))) & 0xfffffff0;
		D = ((D << key_rnd_shift[i]) | (D >> (28-key_rnd_shift[i]))) & 0xfffffff0;

		if (mode == DES_DECRYPT)
			to_gen = 15 - i;
		else
			to_gen = i;
		for (j = 0; j < 6; ++j)
			schedule[to_gen][j] = 0;
		for (j = 0; j < 24; ++j)
			schedule[to_gen][j/8] |= BITNUMINTR(C,key_compression[j],7 - (j%8));
		for ( ; j < 48; ++j)
			schedule[to_gen][j/8] |= BITNUMINTR(D,key_compression[j] - 27,7 - (j%8));
	}
}

void des_crypt(const BYTE in[], BYTE out[], const BYTE key[][6])
{
	WORD state[2],idx,t;

	IP(state,in);

	for (idx=0; idx < 15; ++idx) {
		t = state[1];
		state[1] = f(state[1],key[idx]) ^ state[0];
		state[0] = t;
	}
	state[0] = f(state[1],key[15]) ^ state[0];

	InvIP(state,out);
}

void three_des_key_setup(const BYTE key[], BYTE schedule[][16][6], DES_MODE mode)
{
	if (mode == DES_ENCRYPT) {
		des_key_setup(&key[0],schedule[0],mode);
		des_key_setup(&key[8],schedule[1],!mode);
		des_key_setup(&key[16],schedule[2],mode);
	}
	else {
		des_key_setup(&key[16],schedule[0],mode);
		des_key_setup(&key[8],schedule[1],!mode);
		des_key_setup(&key[0],schedule[2],mode);
	}
}

void three_des_crypt(const BYTE in[], BYTE out[], const BYTE key[][16][6])
{
	des_crypt(in,out,key[0]);
	des_crypt(out,out,key[1]);
	des_crypt(out,out,key[2]);
}

/* --- shim exposed to ctypes: ECB over a whole buffer, in place --- */
void qq_des_ecb(unsigned char *buf, int len, const unsigned char key[8], int mode) {
    BYTE schedule[16][6];
    des_key_setup(key, schedule, mode == 0 ? DES_ENCRYPT : DES_DECRYPT);
    for (int i = 0; i < len; i += 8) {
        des_crypt(buf + i, buf + i, schedule);
    }
}
"""


def _lib_ext():
    system = platform.system()
    if system == "Windows":
        return ".dll"
    if system == "Darwin":
        return ".dylib"
    return ".so"


def _build_or_load_des_lib(debug: bool = False):
    """Compile the embedded (buggy) DES C source into a shared library the
    first time this runs, then cache it next to this script for reuse."""
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qq_des_cache")
    os.makedirs(cache_dir, exist_ok=True)
    lib_path = os.path.join(cache_dir, "qqdes" + _lib_ext())

    if os.path.exists(lib_path):
        if debug:
            print(f"[DEBUG] Reusing cached DES library: {lib_path}")
    else:
        if debug:
            print(f"[DEBUG] No cached DES library found at {lib_path} - "
                  f"compiling now (one-time cost).")
        t0 = time.perf_counter()
        with tempfile.TemporaryDirectory() as tmp:
            h_path = os.path.join(tmp, "des.h")
            c_path = os.path.join(tmp, "des.c")
            with open(h_path, "w") as f:
                f.write(_DES_H_SRC)
            with open(c_path, "w") as f:
                f.write(_DES_C_SRC)

            # Each candidate is an argv *prefix* - some tools (zig) act as a
            # compiler only via a subcommand ("zig cc ...").
            candidates = [
                ["cc"],
                ["gcc"],
                ["clang"],
                ["zig", "cc"],
                ["tcc"],
            ]
            compiler_prefix = None
            for prefix in candidates:
                if _which(prefix[0]):
                    compiler_prefix = prefix
                    break
            if compiler_prefix is None:
                raise RuntimeError(
                    "No C compiler found on PATH (tried cc, gcc, clang, "
                    "zig cc, tcc). QQ Music's QRC lyrics require reproducing "
                    "its buggy DES exactly, which needs a real compiler.\n"
                    "If you just installed one (e.g. `winget install "
                    "zig.zig` or `winget install -e --id LLVM.LLVM`), open a "
                    "*new* terminal/PowerShell window first - PATH changes "
                    "from an installer don't apply to windows that were "
                    "already open. You can check with `zig version` or "
                    "`clang --version` in a fresh terminal."
                )

            cmd = compiler_prefix + ["-O2", "-fPIC", "-shared", "-I", tmp, "-o", lib_path, c_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(
                    f"Failed to compile bundled DES implementation with "
                    f"{' '.join(compiler_prefix)}:\n{result.stderr}"
                )
        if debug:
            print(f"[DEBUG] Compile took {time.perf_counter() - t0:.2f}s "
                  f"(one-time only - cached at {lib_path} from now on).")

    lib = ctypes.CDLL(lib_path)
    lib.qq_des_ecb.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    lib.qq_des_ecb.restype = None
    return lib


def _which(cmd):
    import shutil
    return shutil.which(cmd)


_DES_LIB = None


def _qq_des_ecb(data: bytes, key: bytes, mode: int, debug: bool = False) -> bytes:
    """mode: 0 = encrypt, 1 = decrypt. Uses QQ's buggy DES, ECB, in place."""
    global _DES_LIB
    if _DES_LIB is None:
        _DES_LIB = _build_or_load_des_lib(debug=debug)
    buf = ctypes.create_string_buffer(data, len(data))
    _DES_LIB.qq_des_ecb(buf, len(data), key, mode)
    return buf.raw


def qq_des_decrypt(data: bytes, debug: bool = False) -> bytes:
    """
    Reverse QQ Music's QRC obfuscation pipeline using QQ's own (buggy) DES:
    DES-decrypt(key1) -> DES-encrypt(key2) -> DES-decrypt(key3), ECB mode.
    """
    step1 = _qq_des_ecb(data, QRC_KEY1, mode=1, debug=debug)   # decrypt
    step2 = _qq_des_ecb(step1, QRC_KEY2, mode=0, debug=debug)  # encrypt
    step3 = _qq_des_ecb(step2, QRC_KEY3, mode=1, debug=debug)  # decrypt
    return step3


# --------------------------------------------------------------------------
# QQ Music API calls ()
# --------------------------------------------------------------------------

def search_song(song_name: str, artist: str, debug: bool = False):
    """Search for a track and return its songmid/songid/title/singer."""
    query = f"{song_name} {artist}".strip()
    payload = {
        "comm": {
            "g_tk": 5381,
            "uin": 1152921504916411742,
            "format": "json",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "h5",
            "needNewCode": 1,
            "ct": 23,
            "cv": 0,
        },
        "req_1": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "num_per_page": 10,
                "page_num": 1,
                "query": query,
                "search_type": 0,
            },
        },
    }
    t0 = time.perf_counter()
    resp = _SESSION.get(
        SEARCH_URL,
        params={"data": json.dumps(payload)},
        timeout=10,
    )
    if debug:
        print(f"[DEBUG] Search request took {time.perf_counter() - t0:.2f}s")

    if debug:
        print(f"\n[DEBUG] HTTP status: {resp.status_code}")
        print(f"[DEBUG] Response headers: {dict(resp.headers)}")
        print(f"[DEBUG] Raw response body (first 2000 chars):\n{resp.text[:2000]}\n")

    resp.raise_for_status()

    try:
        data = resp.json()
    except ValueError as e:
        if debug:
            print(f"[DEBUG] JSON parse failed: {e}")
        return None

    top_code = data.get("req_1", {}).get("code")
    body_code = data.get("req_1", {}).get("data", {}).get("code")
    if debug:
        print(f"[DEBUG] req_1.code = {top_code}, body.code = {body_code}")

    try:
        song_list = data["req_1"]["data"]["body"]["song"]["list"]
    except (KeyError, TypeError) as e:
        if debug:
            print(f"[DEBUG] Could not walk to song list: {e}")
            print(f"[DEBUG] Full parsed JSON:\n{json.dumps(data, ensure_ascii=False, indent=2)[:3000]}")
        song_list = []

    if not song_list:
        return None

    top = song_list[0]
    return {
        "songmid": top.get("mid"),
        "songid": top.get("id"),
        "title": top.get("title") or top.get("name"),
        "singer": ", ".join(s.get("name", "") for s in top.get("singer", [])),
    }


def fetch_qrc_raw(songmid: str, songid: int, debug: bool = False):
    """Fetch the raw (still-encrypted) QRC blob for a song."""
    params = {
        "version": "15",
        "miniversion": "82",
        "lrctype": "4",
        "musicid": songid,
    }
    t0 = time.perf_counter()
    resp = _SESSION.get(QRC_URL, params=params, timeout=10)
    if debug:
        print(f"[DEBUG] QRC request took {time.perf_counter() - t0:.2f}s")

    if debug:
        print(f"\n[DEBUG] QRC HTTP status: {resp.status_code}")
        print(f"[DEBUG] QRC response headers: {dict(resp.headers)}")
        print(f"[DEBUG] QRC raw response body (first 2000 chars):\n{resp.text[:2000]}\n")

    resp.raise_for_status()
    text = resp.text.strip()

    match = re.search(
        r"<content[^>]*>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</content>",
        text,
        re.S,
    )
    if match:
        hex_blob = match.group(1).strip()
    else:
        candidate = text.strip()
        if re.fullmatch(r"[0-9A-Fa-f]+", candidate) and len(candidate) > 100:
            hex_blob = candidate
            if debug:
                print("[DEBUG] No <content> wrapper found, but body is a "
                      "raw hex blob - using it directly.")
        else:
            if debug:
                print("[DEBUG] No <content> tag found and body doesn't look "
                      "like a raw hex blob either - endpoint likely "
                      "returned an error page or empty response.")
            return None

    if not hex_blob or hex_blob == "0":
        if debug:
            print(f"[DEBUG] Hex blob is empty/placeholder: {hex_blob!r}")
        return None
    return hex_blob


def decode_qrc(hex_blob: str, debug: bool = False) -> str:
    """Turn the hex-encoded, DES+zlib obfuscated blob into QRC XML text."""
    t0 = time.perf_counter()
    raw = binascii.unhexlify(hex_blob)
    decrypted = qq_des_decrypt(raw, debug=debug)
    decompressed = zlib.decompress(decrypted)
    if debug:
        print(f"[DEBUG] DES decrypt + zlib inflate took "
              f"{time.perf_counter() - t0:.4f}s (this part is never the "
              f"bottleneck - it's pure local compute).")
    return decompressed.decode("utf-8", errors="ignore")


def parse_qrc_lines(qrc_xml: str):
    """
    Parse QRC XML into a list of (line_start_ms, line_duration_ms, words)
    where words is a list of (text, start_ms, duration_ms).
    """
    lines = []
    line_pattern = re.compile(r"\[(\d+),(\d+)\](.*?)(?=\[\d+,\d+\]|$)", re.S)
    word_pattern = re.compile(r"(.*?)\((\d+),(\d+)\)")

    for line_start, line_dur, body in line_pattern.findall(qrc_xml):
        words = []
        for text, w_start, w_dur in word_pattern.findall(body):
            if text:
                words.append((text, int(w_start), int(w_dur)))
        if words:
            lines.append((int(line_start), int(line_dur), words))
    return lines


def fetch_plain_lrc(songmid: str, debug: bool = False) -> str:
    """Fallback: fetch plain line-level LRC lyrics."""
    params = {
        "nobase64": "1",
        "songmid": songmid,
        "g_tk": "5381",
        "loginUin": "0",
        "hostUin": "0",
        "format": "json",
        "inCharset": "utf8",
        "outCharset": "utf-8",
        "notice": "0",
        "platform": "yqq.json",
        "needNewCode": "0",
    }
    t0 = time.perf_counter()
    resp = _SESSION.get(LYRIC_FALLBACK_URL, params=params, timeout=10)
    if debug:
        print(f"[DEBUG] Plain-LRC fallback request took {time.perf_counter() - t0:.2f}s")
    resp.raise_for_status()
    try:
        data = resp.json()
    except ValueError:
        return ""
    return data.get("lyric", "")


def ms_to_timestamp(ms: int) -> str:
    minutes = ms // 60000
    seconds = (ms % 60000) / 1000
    return f"{minutes:02d}:{seconds:05.2f}"


def get_qrc_lyrics(song_name: str, artist: str = "", debug: bool = False) -> dict:
    """
    Programmatic entry point for use from another app (e.g. a multi-source
    lyrics fetcher / fallback chain) instead of the interactive CLI below.

    Returns a dict:
        {
            "source": "qrc" | "lrc" | None,
            "title": str, "singer": str, "songmid": str, "songid": int,
            "lines": [(line_start_ms, line_dur_ms, [(word, w_start_ms, w_dur_ms), ...]), ...]  # only for "qrc"
            "lrc": str,  # only for "lrc"
        }
    or {"source": None} if nothing was found. Reuses one requests.Session
    and the compiled DES library across calls, so calling this repeatedly
    in a long-running process is much cheaper than re-invoking the script
    per song - most of the cost is the two network round-trips to QQ, not
    the local decrypt/decode step.
    """
    result = search_song(song_name, artist, debug=debug)
    if not result or not result.get("songmid"):
        return {"source": None}

    out = {
        "title": result["title"],
        "singer": result["singer"],
        "songmid": result["songmid"],
        "songid": result["songid"],
    }

    hex_blob = None
    try:
        hex_blob = fetch_qrc_raw(result["songmid"], result["songid"], debug=debug)
    except requests.RequestException:
        hex_blob = None

    if hex_blob:
        try:
            qrc_xml = decode_qrc(hex_blob, debug=debug)
            out["raw_qrc_xml"] = qrc_xml  # unparsed - inspect this for anything the regex parser drops
            lines = parse_qrc_lines(qrc_xml)
            if lines:
                out["source"] = "qrc"
                out["lines"] = lines
                return out
        except Exception:
            pass

    lrc = fetch_plain_lrc(result["songmid"], debug=debug)
    if lrc:
        out["source"] = "lrc"
        out["lrc"] = lrc
        return out

    out["source"] = None
    return out


def main():
    print("QQ Music word-by-word (QRC) lyrics fetcher")
    print("-" * 45)
    song_name = input("Song name: ").strip()
    artist = input("Artist name: ").strip()

    if not song_name:
        print("Song name is required.")
        return

    debug = input("Enable debug output? (y/N): ").strip().lower() == "y"
    t_total = time.perf_counter()

    print(f"\nSearching for '{song_name}' by '{artist}'...")
    result = search_song(song_name, artist, debug=debug)
    if not result or not result.get("songmid"):
        print("No matching track found on QQ Music.")
        print("(Re-run and answer 'y' to the debug prompt to see the raw "
              "API response and figure out why.)")
        return

    print(f"Found: {result['title']} - {result['singer']} "
          f"(mid={result['songmid']}, id={result['songid']})\n")

    hex_blob = None
    try:
        hex_blob = fetch_qrc_raw(result["songmid"], result["songid"], debug=debug)
    except requests.RequestException as e:
        print(f"QRC request failed: {e}")

    lines = None
    if hex_blob:
        try:
            qrc_xml = decode_qrc(hex_blob, debug=debug)

            # Dump the raw, UN-parsed decrypted XML to a file so we can
            # inspect it for anything our text(start,dur) regex parser
            # might be silently discarding - e.g. duet/voice-role markers
            # that don't fit that exact shape (they wouldn't show up in
            # the word-by-word output above even if QQ does encode them).
            dump_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f"raw_qrc_{result['songmid']}.xml",
            )
            with open(dump_path, "w", encoding="utf-8") as f:
                f.write(qrc_xml)
            print(f"[Raw decrypted QRC XML saved to: {dump_path}]")
            print("(Open that file and search it for anything like 合/女/男/"
                  "duet/v1/v2/bg markers - if they're in there, they're in "
                  "there in a shape our parser isn't expecting yet.)\n")

            lines = parse_qrc_lines(qrc_xml)
        except Exception as e:
            print(f"Failed to decode QRC blob ({e}); falling back to plain LRC.\n")
            lines = None
    else:
        print("No QRC (word-by-word) lyrics available for this track; "
              "falling back to plain LRC.\n")

    if lines:
        print("=== Word-by-word (QRC) lyrics ===\n")
        for line_start, _line_dur, words in lines:
            line_text = "".join(w[0] for w in words)
            ts = ms_to_timestamp(line_start)
            print(f"[{ts}] {line_text}")
            word_detail = "  ".join(
                f"{w_text}@{w_start}ms" for w_text, w_start, _w_dur in words
            )
            print(f"        {word_detail}")
        print(f"\n(total time: {time.perf_counter() - t_total:.2f}s)")
        return

    lrc = fetch_plain_lrc(result["songmid"], debug=debug)
    if not lrc:
        print("No lyrics found for this track (plain or QRC).")
        print(f"\n(total time: {time.perf_counter() - t_total:.2f}s)")
        return

    print("=== Line-level (LRC) lyrics ===\n")
    print(lrc)
    print(f"\n(total time: {time.perf_counter() - t_total:.2f}s)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")