# Setup
**1. Install Python dependencies**
First, make sure you have Python 3.7+ installed. Then, install the required Python packages:

pip install -r requirements.txt


**2. Run the Flask Application**
python app.py

The application will start a development server at http://localhost:5000.


**3. Dockerize the Application**
You can use the provided Dockerfile to containerize the application. Follow these steps to build and run the Docker container:

**Build the Docker image:**

docker build -t yolov8-app .

Run the Docker container:

docker run -p 5000:5000 yolov8-app

The application will be running on http://localhost:5000.

**4. Docker Commands**

To stop the container, use:
docker stop <container_id>

To remove the container:
docker rm <container_id>

**5. Example Image**

![Example Image](/uploads/Ex1.png)
![Example Image](/uploads/Ex2.png)




