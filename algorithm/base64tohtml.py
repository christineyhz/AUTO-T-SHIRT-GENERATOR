# This is the function which takes in a base64 image string, and write an <img> tag to a html file 
def base64toimg(base64):
    open('./templates/base_saved_design.html', 'w').close() #This clear the file's content first
    f = open('./templates/base_saved_design.html','w')
    message = """<img src=" """

    f.write(message)

    message = base64

    f.write(message)

    message = """ " alt="Saved Design">"""

    f.write(message)
    f.close()
