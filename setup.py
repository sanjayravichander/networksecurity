from setuptools import find_packages,setup
from typing import List

def getrequirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str]=[]
    try:
        with open('requirements.txt','r') as f:
            lines=f.readlines()
            for line in lines:
                requirement=line.strip()
                # Ignore - e.
                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("File not found")
    return requirement_list

# print(getrequirements()) --> checking whether it is working fine or not

setup(
    name="networksecurity",
    version="0.0.1",
    author="sanjayravichander",
    author_email="sanjay.1991999@gmail.com",
    packages=find_packages(),
    install_requires=getrequirements(),
)
