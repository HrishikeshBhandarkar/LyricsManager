from setuptools import setup, find_packages

setup(
    name="lyric-manager",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "click>=8.0.0",
        "mutagen>=1.47.0",
        "requests>=2.31.0",
        "syncedlyrics>=0.7.0",
    ],
    extras_require={
        "ai": [
            "torch>=2.0.0",
            "torchaudio>=2.0.0",
            "whisperx>=3.1.0",
            "demucs>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "lyric_manager=Lyrics_manager.cli:main",
            "lyric-manager=Lyrics_manager.cli:main",
        ],
    },
    description="A top-tier interactive CLI for fetching and AI-generating synced lyrics",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
