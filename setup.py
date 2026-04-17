from setuptools import setup, find_packages

setup(
    name="cogcal1",
    version="1.0.0",
    author="Bhupesh Chandra Dimri",
    description="CogCal-1: Confidence Calibration Under Epistemic Uncertainty — A Metacognition Benchmark for Frontier Language Models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bhupeshcdimri/CogCal-1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
    ],
    extras_require={
        "eval": [
            "anthropic>=0.25.0",
            "openai>=1.0.0",
            "google-generativeai>=0.5.0",
            "mistralai>=0.4.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "pandas>=2.0.0",
        ],
        "dev": [
            "pytest>=7.4.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
    ],
    keywords="LLM calibration benchmark metacognition AGI evaluation ECE confidence",
)
