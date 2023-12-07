# Log Reader to MQTT Dockerized Application

This project is a Dockerized Python application that reads logs from a specified Docker container and sends messages to an MQTT broker based on specified keywords.

## Prerequisites

Before running the application, ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repository
    ```

3. Create a `.env` file in the project root and set the required environment variables:

    ```env
    MQTT_BROKER_HOST=your_mqtt_broker_host
    MQTT_BROKER_PORT=your_mqtt_broker_port
    MQTT_USERNAME=your_mqtt_username
    MQTT_PASSWORD=your_mqtt_password
    MQTT_TOPIC=your_mqtt_topic
    CONTAINER_ID_TO_READ=your_container_id
    KEYWORDS=your_keywords_separated_by_commas
    ```

4. Build and run the Docker Compose service:

    ```bash
    docker-compose up -d
    ```

The application will start monitoring logs from the specified Docker container and send MQTT messages based on specified keywords.

## Customization

You can customize the application behavior by modifying the environment variables in the `.env` file. Refer to the `docker-compose.yml` and `log_reader.py` files for available options.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
