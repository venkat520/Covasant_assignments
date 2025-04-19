from flask import Flask, jsonify, g 
from flask import render_template, request 

app=Flask(__name__)

notesdata="information.txt"
@app.route("/updatefortoday", methods=['GET','POST'])          #http://localhost:5000/updatefortoday
def home():
    if request.method=='POST':
        notes=request.form.get("text",'')
        with open(notesdata,'a') as file:
            file.write(notes.strip()+'\n')
        return 'Successfully updated data'
    
    return """
           <html>
           <head>
           <title>sharing of content</title>
           </head>
           <body>
           <center><h1>WRITE SOMETHING HERE</h1></center>
           <form action="/updatefortoday" method="post">
           <center><textarea rows="20" cols="80" name="text" ></textarea></center>
           <br/>
            <br/>
           <center><input type="submit" value="Submit" /></center>
           </form>
           
           </body>
           </html>
           """


@app.route("/share", methods=['GET'])  # http://localhost:5000/share
def share():
    with open(notesdata, 'r') as file:
        notes = file.read()  
    return f"<html><body><h1>Notes:</h1><pre>{notes}</pre></body></html>"
    

@app.route("/clearnotepadtxt", methods=['GET'])  # http://localhost:5000/clearnotepadtxt
def clear_notepad_txt():
    with open(notesdata, 'w') as file:
        file.write('')  
    return "Successfully cleared the notes"


if __name__=='__main__':
    app.run()                        #http://localhost:5000