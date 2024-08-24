# Lambda - COVID Tweet Search Engine

Search Engine Lambda was built to dissect twitter data to analyze government and public
attitudes towards Covid and vaccines. Tweet data from the USA, India, and Mexico have
been analyzed for three languages namely English, Hindi, and Spanish.

[Live Demo](https://tw-lambda.netlify.app/search)

Video Demo - [https://www.youtube.com/watch?v=-z5HASjF3dQ&t=2s](https://www.youtube.com/watch?v=-z5HASjF3dQ&t=2s)

**For server build**

1. Change working directory to `web-server/betasearch`

2. Install required python modules `pip3 install django djangorestframework django-cors-headers googletrans==4.0.0-rc1 google-cloud-language pysolr tweepy GoogleNews`

3. Run `python3 manage.py runserver`

**For Client build**

1. Change working directory to `client`

2. Install Node version v14

3. Run `npm install` in this folder to initialize node modules or to update packages

4. For a development build run `npm run serve`

5. Open `localhost:8080` to see the app up and running

**Tech Stack used**

Frontend → VueJS

Backend → Python + Django

Search Platform → Solr

Hosting → AWS EC2

Analytics → Highcharts

Sentiment Analysis → Google Natural Language AI

**Sample Screenshots**

<img width="1437" alt="Screenshot 2024-08-23 at 8 30 31 PM" src="https://github.com/user-attachments/assets/d597ed53-13a1-4349-a2bc-38a44af9615a">

<img width="1440" alt="Screenshot 2024-08-23 at 8 31 02 PM" src="https://github.com/user-attachments/assets/e3dc96aa-4c1a-4c9b-8ca0-75faf8c197fc">




**Team Members**

1. Muhamed Aashiq

2. Kaviarasu

3. Deepak

4. Dayashankar
