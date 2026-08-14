from setuptools import setup, find_packages

setup(
    name="lyric-manager",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "click>=8.0.0"
    ],
    entry_points={
        "console_scripts": [
            "lyric_manager=Lyrics_manager.cli:main",
        ],
    },
    description="A top-tier interactive CLI for fetching and AI-generating synced lyrics",
)
