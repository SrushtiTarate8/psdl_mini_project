import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from serpapi import GoogleSearch
import speech_recognition as sr
from gtts import gTTS
import os
from transformers import pipeline
import requests
import speech_recognition as sr
import pyttsx3
import pandas as pd
import sqlite3



def search_topic_web(topic):
    params = {
        "engine": "google",
        "q": topic,
        "api_key": "f9d7600765e1e9cb498b928fc30e6bad3948c4652c46323ca050d3aa183f5cd8"  
    }


    search = GoogleSearch(params)
    results = search.get_dict()
    links = results.get("organic_results", [])

    print(f"\n🔍 Top Results for '{topic}':\n")
    for result in links[:5]:  # Top 5
        print(f"- {result.get('title')}")
        print(f"  {result.get('link')}")
        print(f"  {result.get('snippet')}\n")

def search_youtube(subject):
    videosSearch = VideosSearch(f"{subject} course", limit=5)
    
    print(f"\n🎥 Top YouTube Videos for '{subject}':\n")
    for video in videosSearch.result()['result']:
        title = video['title']
        link = video['link']
        print(f"- {title}\n  {link}\n")

def scrape_gfg(subject):
    # Convert the subject to a format suitable for URL
    query = subject.replace(" ", "+")
    url = f"https://www.geeksforgeeks.org//?s={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve GeeksforGeeks results.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find article links on the page
    articles = soup.find_all('div', class_='head')
    
    print(f"\n📚 Top GeeksforGeeks Articles for '{subject}':\n")
    for a in articles[:5]:  # Only top 5 results
        link = a.find('a')
        if link:
            print(f"- {link.text.strip()}\n  {link['href']}\n")

import sqlite3
import matplotlib.pyplot as plt

def fetch_student_results():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()
    cur.execute("SELECT course, marks_ob, full_marks FROM result")
    data = cur.fetchall()
    con.close()
    return data

def visualize_marks_distribution():
    # Fetching student results
    data = fetch_student_results()

    # Dictionary to store course-wise marks data
    course_marks = {}

    # Process the data
    for row in data:
        course = row[0]
        marks_obtained = float(row[1])
        full_marks = float(row[2])
        percentage = (marks_obtained / full_marks) * 100
        
        if course not in course_marks:
            course_marks[course] = []
        course_marks[course].append(percentage)
    
    # Plotting Bar charts for each course's performance distribution
    for course, marks in course_marks.items():
        plt.figure(figsize=(8, 5))
        plt.hist(marks, bins=10, edgecolor='black')
        plt.title(f"Distribution of Marks for {course}")
        plt.xlabel("Percentage Marks")
        plt.ylabel("Number of Students")
        plt.grid(True)
        plt.show()

def visualize_pass_fail():
    # Fetching student results
    data = fetch_student_results()

    pass_count = 0
    fail_count = 0

    for row in data:
        marks_obtained = float(row[1])
        full_marks = float(row[2])
        percentage = (marks_obtained / full_marks) * 100
        
        if percentage >= 40:  # Assuming pass percentage is 40%
            pass_count += 1
        else:
            fail_count += 1

    # Pie chart for pass vs fail distribution
    labels = 'Pass', 'Fail'
    sizes = [pass_count, fail_count]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Pass vs Fail Distribution')
    plt.show()

engine = pyttsx3.init()

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"🧑 You said: {query}")
        return query
    except sr.UnknownValueError:
        print("❌ Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("❌ Speech Recognition service error.")
        return None

def ask_mistral(prompt):
    """Send prompt to local Mistral model and get response."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        print("Mistral Response Status:", response.status_code)
        result = response.json().get("response", "")
        print("🤖 Mistral says:", result.strip())
        return result.strip()
    except Exception as e:
        print("❌ Mistral request failed:", e)
        return "Sorry, I couldn't connect to Mistral."

def chat():
    """Full chat loop between User and Mistral."""
    while True:
        user_query = listen()
        if user_query:
            if "exit" in user_query.lower():
                speak("Goodbye!")
                break

            mistral_reply = ask_mistral(user_query)
            speak(mistral_reply)



def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Search a Topic")
        print("2. Perform Analysis")
        print("3. Exit")
        print("4. Ask a query")
        print("5. Add bulk student data from excel to database")
        
        choice = input("Please enter your choice (1/2/3/4/5): ")

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again.")

def import_students_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)  # You can use read_csv if the file is CSV

    # Connect to the database
    con = sqlite3.connect('rms.db')
    cur = con.cursor()

    # Loop through each row and insert into student table
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO student (name, email, gender, dob, contact, admission, course, state, city, pin, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['name'], row['email'], row['gender'], row['dob'],
            row['contact'], row['admission'], row['course'],
            row['state'], row['city'], row['pin'], row['address']
        ))

    # Commit and close
    con.commit()
    con.close()
    print(f"✅ Successfully imported {len(df)} students!")


            
def handle_search_topic():
    subject = input("Enter the subject: ").strip()
    scrape_gfg(subject)
    search_youtube(subject)
    search_topic_web(subject)

def handle_analysis():
    visualize_marks_distribution()
    visualize_pass_fail()
    fetch_student_results()

def handle_chat():
    while True:
        user_query = listen()
        if user_query:
            if "exit" in user_query.lower():
                speak("Goodbye")
                break
            response = ask_mistral(user_query)
            speak(response)


menu_actions = {
    "1": handle_search_topic,
    "2": handle_analysis,
    "3": exit,
    "4": handle_chat,
    "5": lambda: import_students_from_excel(r"C:\Users\usidh\OneDrive\Desktop\students.xlsx")

}

        
        # Execute the selected function


# Run the main menu
main_menu()
