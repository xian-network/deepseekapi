from setuptools import setup, find_packages


setup(
    name='DeepSeek API',
    version='1.0.0',
    author='crosschainer',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'aiohttp', 'fastapi', 'uvicorn', 'pydantic', 'python-dotenv', 'ujson', 'python-multipart'
    ],
)
