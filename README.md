# AI-powered-Resume-Analyzer-and-Feedback-Generator

____________________________________________________________________________________________________________________________________________
  ### ---UPDATE: Version 1.0 has a planned release on November 1st, 2023. I am wrapping up my testing to ensure a robust MVP (v1.0). Once v1.0 is released, I will begin improving the overall user experience by doing the following... 
 1. Creating a more engaging front-end web interface
 2. Continue to thoroughly test and debug
 3. Expand functionality through various channels such as... Resume generation based on job description, improved feedback, structured feedback parameters, resume rating scale, etc
____________________________________________________________________________________________________________________________________________

## Description

The project is designed as an innovative solution that aids job seekers in refining and enhancing their resumes by leveraging state-of-the-art machine learning capabilities. Through this system, users can upload their resumes and receive constructive feedback that can significantly improve their chances of standing out to potential employers.

At the heart of the system lies the back-end, constructed using the Flask web framework. This back-end handles several vital functionalities:

Receiving and processing user-uploaded resumes, converting these from PDF format into textual content.
Interacting with OpenAI's GPT-4 model to analyze the extracted resume content and generate detailed feedback.
Ensuring robust error handling to manage unexpected scenarios, from corrupt PDF files to potential API-related issues, all the while maintaining the integrity and security of user data.
Complementing this robust back-end is a front-end built entirely from scratch. Making use of the triad of web development - HTML, CSS, and JavaScript - the front-end provides users with an intuitive and responsive interface. The interface allows them to easily upload their resumes, view the feedback generated, and make necessary changes based on the suggestions provided.

A core tenet that underscored the development of this project was the Test-Driven Development (TDD) approach. Before any feature was implemented, tests were designed to dictate the desired functionality and ensure reliability. This approach not only provided a clear development roadmap but also ensured that each feature was thoroughly vetted for functionality and reliability before being integrated. Consequently, this resulted in a system that's both reliable and user-centric.

In essence, this project serves as a prime example of how modern web development practices, combined with cutting-edge AI models, can create value-added solutions that cater to real-world needs. Whether it's a fresh graduate looking to make their mark or an experienced professional aiming to switch careers, this platform offers invaluable assistance in putting their best foot forward in the competitive job market.

## Getting Started

### Dependencies

* aiohttp==3.8.5
* aiosignal==1.3.1
* async-timeout==4.0.3
* attrs==23.1.0
* certifi==2022.12.7
* charset-normalizer==3.1.0
* click==8.1.3
* Flask==2.2.3
* Flask-Cors==3.0.10
* frozenlist==1.4.0
* idna==3.4
* importlib-metadata==6.6.0
* itsdangerous==2.1.2
* Jinja2==3.1.2
* lxml==4.9.2
* MarkupSafe==2.1.2
* multidict==6.0.4
* openai==0.28.1
* PyPDF2==3.0.1
* python-docx==0.8.11
* python-dotenv==1.0.0
* requests==2.28.2
* six==1.16.0
* tqdm==4.66.1
* typing_extensions==4.5.0
* urllib3==1.26.15
* Werkzeug==2.2.3
* yarl==1.9.2
* zipp==3.15.0

### Installing

1. Clone the repository:
```
git clone [your-repo-link]
```

2. Navigate to the directory:
```
cd [your-repo-name]
```

3. Create a virtual environment (Optional but recommended):
```
python -m venv venv
```

4. Activate the virtual environment:

    On Windows:
    ```
    venv\Scripts\activate
    ```
    On MacOS and Linux:
    ```
    source venv/bin/activate
    ```

5. Install the dependencies:
```
pip install -r requirements.txt
```

### Executing program

    
  Using python app.py:
  ```
  python app.py
  ```

  Using flask run:
  ```
  export FLASK_APP=app.py  # MacOS/Linux
  set FLASK_APP=app.py  # Windows
  export FLASK_ENV=development  # MacOS/Linux
  set FLASK_ENV=development  # Windows
  ```
  
  Then, run the Flask application:
  ```
  flask run
  ```

## Help

1. Ensure all dependencies are installed: pip install -r requirements.txt.
2. Ensure your virtual environment is activated.
3. Check the logs for any specific error messages and try searching for them online.

For more assistance or to report bugs, please open an issue on this repository.

## Authors

Brian Bell
[@BrianBe11](https://www.linkedin.com/in/brianbe11/)

## Version History

* 1.0
    * Various bug fixes and optimizations
    * Improve overall code & comment readability
    * Various high level tests added (Unit, API, etc)
    * See [commit change]() or See [release history]()
* 0.7
    * Various bug fixes and optimizations
    * Updated used GPT version to 'gpt-3.5-turbo'
    * Improve overall code & comment readability
    * See [commit change]() or See [release history]()
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

