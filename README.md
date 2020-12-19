## tri-link

This web application is built using Django, serving to demonstrate a way to build a SaaS application with monthly subscription payments using Stripe.  

“Type Beats” are a popular marketing strategy for users uploading their music to YouTube. A popular format for these videos that are uploaded are a background image, with an audio spectrum matching to the beat of the song.  

Normally a user would need a program such as Adobe After Effects to create a mp4 video with an accurate audio spectrum. The aim of this project here, dubbed “tri-link” is a way for users to subscribe for a monthly fee to use the service which is to programmatically create mp4 videos that contain a background image, and an audio spectrum based off a user uploaded file.  

This project is only used to serve as a demo demonstrating the use of Django, for practicality reasons the code that renders videos would need to be executed elsewhere on a dedicated server/serverless function to not bog down the front end 😊.  

The projects core code that is responsible for programmatically creating the videos is based off an open-source project found here https://github.com/ravenkls/Visualise  
