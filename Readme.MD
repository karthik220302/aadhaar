# Aadhaar Adress Update

This is a project developed to update the Aadhaar address of users not having any proper Proof-Of-Address(POA) documents.
In order to overcome this we are introducing a new mean in which the houseowner/landlord can help the users to update the address by providing their address linked with the Aadhaar.

## What Have we done
we designed this app/webapp suitable for both mobile and laptop/computers , key features of this project is that we made this
to use less date and in a more secure way enabling end-to-end encrytion of datas given by both the user and the landlord/houseowner.
This also provides the feature of notifying the user in every process and stores the log for each and every step .
We also provide Multi-lingual(Multi language) support so that people can access our webapp all over India.

## Getting Started
First clone the repository or Download the zip file and extract the file in your project directory .

### Prerequisites

Requirements for the software and other tools to build, test and push
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)

### Installation for Windows

make sure you downloaded and extracted the zip and now open terminal from the same directory

first install the virtual environment

    pip install virtualenv

then create a virtual environment

    python -m venv venv  

And now activate the virtual environment

    venv/scripts/activate

finally install the requirements

    pip install -r requirements

 ### Installation for Linux/Unix

make sure you downloaded and extracted the zip and now open terminal from the same directory


first install the virtual environment

    pip3 install virtualenv

then create a virtual environment

    python3 -m venv venv    

And now activate the virtual environment

    source venv/bin/activate

finally install the requirements

    pip install -r requirements   

 ### Installation for Mac

make sure you downloaded and extracted the zip and now open terminal from the same directory

first install the virtual environment

    pip3 install virtualenv

then create a virtual environment

    python3 -m venv venv    

And now activate the virtual environment

    source venv/bin/activate

finally install the requirements

    pip install -r requirements   


## Running the app

Last step remaining in this process is to run the app

make sure you are the project directory and having venv activated

    flask run

### Now open the link generated in the terminal and the webapp is ready to use



## API used

-[EKYC-offline API](https://github.com/uidaitc) -used for EKYC process

-[Opencage geolocator](https://opencagedata.com/) - used for geolocating

## Built With

  - [python](https://www.python.org/) - Used for the backend

  - [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Used to connect the front-end and back-end

  - [html/css/bootstrap](https://getbootstrap.com/) - Used for the frontend


 ## requirements and uses

  - [cryptography]() - Used for the end-to-end encryption of datas

  - [pymongo]() - Used to connect the mongodb with flask

  - [gunicorn]() - Used to run the flask

  - [DateTime]() - Used to save the logfiles

  - [zipfile36]() - Used to encrypt and decrypt

  - [opencage]() - Used to geolocate

  - [pybase64]() - Used to convert captcha

   - [haversine]() - Used to get coordinates


 ## Contributing

codesploit()

## Versioning

We use [Semantic Versioning](http://semver.org/) for versioning.



## License

This project is licensed under the [CC0 1.0 Universal](LICENSE.md)
Creative Commons License - see the [LICENSE.md](LICENSE.md) file for
details

## Acknowledgments

  - Designed specifically for Aadhaar Hackathon 2021
