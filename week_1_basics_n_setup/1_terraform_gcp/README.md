# Setting up GCP

I decided to go the route of installing Google Cloud via Docker container + volume.

## Step-by-Step Guide With Named Volume

**1. Pull the Google Cloud SDK Docker Image**

Pull the latest Google Cloud SDK Docker image:

```bash
docker pull google/cloud-sdk:latest
```

**2. Create a Docker Volume for Persistent Authentication**

To ensure that your authentication details persist across different container runs, create a Docker volume:

```bash
docker volume create gcloud-config-volume
```

**3. Authenticate with Google Cloud SDK**

Follow the on-screen instructions to authenticate.

**4. Run the Google Cloud SDK container**, mounting the volume you created in the previous step. This binds the authentication data inside the container to the gcloud-config-volume on your host:

```bash
docker run -it --name gcloud-config -v gcloud-config-volume:/root/.config/google-cloud google/cloud-sdk gcloud auth login
```

**5. Running Google Cloud SDK Commands**

After authentication, you can run any gcloud command by starting a container that mounts the gcloud-config-volume. For example, to run an interactive bash shell:

```bash
docker run -it --volumes-from gcloud-config google/cloud-sdk bash
```
Inside this container, you'll have both bash and the gcloud command available.

### Notes

* The authentication details are saved in the gcloud-config-volume volume. You only need to authenticate once, as long as you use this volume in subsequent gcloud container runs.

* Ensure you keep the volume data secure, as it contains your Google Cloud authentication details.

* Set your project like so:
```commandline
docker exec -it gcloud-config gcloud config set project dtc-de-398314
```

## Step-by-Step Guide Without Named Volume

**1. Pull the Google Cloud SDK Docker Image**

Pull the latest Google Cloud SDK Docker image:

```bash
docker pull google/cloud-sdk:latest
```

**2. Authenticate with Google Cloud SDK**

Start the Google Cloud SDK container to initiate the authentication process:

```
docker run -it --name gcloud-config google/cloud-sdk gcloud auth login
```

Follow the on-screen instructions to authenticate.

**3. Running Google Cloud SDK Commands**

Once you've authenticated, you can use the gcloud-config container to run further gcloud commands. For instance, if you want to get the list of compute instances:

```commandline
docker start gcloud-config
docker exec gcloud-config gcloud compute instances list
```

For an interactive bash session with the gcloud command available:

```commandline
docker start gcloud-config
docker exec -it gcloud-config bash
```

### Mounting Google Service Account Credentials to Docker Image

**1. Locate your Service Account JSON Key:**

First, make sure you have your service account key in JSON format. This is typically provided when you create a service account on Google Cloud Console. Let's assume the path to this file on your Windows system is `C:\path\to\your\service-account-key.json`.

**2. Run the Google Cloud SDK Docker Image with a Mounted Volume:**

You'll want to mount the directory containing your service account key to a directory in the container. 

Here's an example:

```bash
docker run -it -v /c/path/to:/tmp/keys google/cloud-sdk:latest /bin/bash
```

This command mounts the `C:\path\to/directory` from your Windows host to `/tmp/keys` inside the Docker container. The `-v` option in docker run is used for volume mounting.

**3. Activate the Service Account Inside the Docker Environment:**

Once you're inside the Docker environment, you can activate the service account using:

```bash
gcloud auth activate-service-account --key-file=/tmp/keys/service-account-key.json
```

After running this command, the gcloud CLI will use this service account for all subsequent commands.

**4. Verification:**

Verify that the service account is now active:

```bash
gcloud auth list
```

This will show you which accounts are currently authenticated in this environment, and the service account should be among them.

**Note:** Be cautious when handling service account keys. They provide access to your GCP resources, so always manage and store them securely. Avoid pushing images that contain your service account keys and always keep them out of public repositories and places where unauthorized individuals might access them.