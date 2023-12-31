# API-Stock-Signalling
###### NOTE: this is a project to practice your Python industry skills. Please upload your solutions by opening a new branch to the main. All files that are instantly merged to the main will be deleted. 
## Overview
A small consultancy who is currently delivering client work for a major bank wants to monitor the prices for the following stocks: Tesla, Apple, Microsoft, Google, and Nike. Once the stock falls below a certain price, they want to be immediately notified so that they can purchase more stocks. 
## Goal
Write a real time Python application that monitors the prices then notifies the user when the price of any of these stocks falls by at least £0.25 GBP. The user should also be notified if today's price is less than the 7-day average of that stock price.
## Brief
To do this, the client has recommended using a popular automation website called IFTTT: https://ifttt.com/. They are willing to use a different provider or solution (use those consultancy skills!) if you believe there is a better option.
#### IFTTT Applet

IFTTT stands for “If This Then That” and it’s an automation platform that allows you to connect different apps and services together. An applet is a connection between two or more apps or devices that enables you to do something that those services couldn’t do on their own. Applets consists of two parts triggers and actions. Triggers tell an applet to start, and actions are the end result of an applet run. To use an applet, you’ll need to create a free IFTTT account and connect your apps and devices to IFTTT so that they can talk to each other.

#### Proposed Workflow
- Write a script that returns the stock prices. This will involve making an API request.
- Set up a IFTTT account and applet. This will be accessible via the mobile app which allows you to trigger the webhook service provided by IFTTT.
- You will need to configure the 'webhooks' service to receive web requests. You can find more details here: https://ifttt.com/maker_webhooks. 
- From here you can write an application that utilises the requests package to make POST and GET requests.
- Think of what aspects or components of your proposed solution needs to be tested and what would these tests look like and attempt to implement such tests.

## Main Considerations
- Choose an automation approach. Are you planning on using IFTTT or another workflow?
- What API are you going to use? You can use this as a starting point: https://github.com/public-apis/public-apis
- Remember, this is a proposed workflow. If you believe you have a more efficient approach please reach out to the Academy Team.
#### Requirements Gathering
The start to any project is to make sure you have clear and well-defined requirements for your project. Most projects start with a vague idea of what the stakeholder wants, and as a consultant, we will never have as much knowledge about their problem/business context as they do. Therefore, we need to get as much information out of them as possible, as they will subconsciously assume that we know everything. For this project, Alex Naylor will be the stakeholder.

If you don't know the answer to any question then you should always ask - NEVER ASSUME. This will only risk the accuracy of your work and end up having to do everything all over again if you wrongly assume.

Questions to ask yourself constantly throughout the project are:

- What is the purpose of this project, why does the stakeholder want this and what is the desired outcome of the project?
- Is there any extra info that the stakeholder could tell you to help tailor the project to what they want?

## Assessment
For the assessment, you will have a 15 minute technical interview. This will consist of a strict 5 minute presentation on your technical solution. There is no need to create slides for this but you may want to demo your code. For the second half of the session, you will be asked technical questions related to the project. You will be assessed on: 
- Project Complexity
- Brief Completness i.e. have you managed to meet the client brief?
- Coding Standards

Good Luck!
