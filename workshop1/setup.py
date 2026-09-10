from setuptools import find_packages, setup
from glob import glob

package_name = 'workshop1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
       ('share/' + package_name + '/config', ['config/parameter.yaml']),
        ('share/' + package_name + '/launch', ['launch/launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abdelaziz',
    maintainer_email='abdelaziz.islam.galal@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtle_controller = workshop1.turtle_controller:main',
            'go_to_goal = workshop1.go_to_goal:main',
            'service_cleintr = workshop1.service_cleintr:main',
        ],
    },
)
