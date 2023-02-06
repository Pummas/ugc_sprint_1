from config import consumer_config, settings
from extractor import KafkaExtractor
from pre_start import create_kafka_topics


def extract_events():
    # для проверки работоспособности
    extractor = KafkaExtractor(settings.TOPIC_NAMES, consumer_config)
    for message_bytes in extractor.fetch():
        print(f"Message consumed: value = {message_bytes}")


if __name__ == "__main__":
    from _producer import write_events

    create_kafka_topics(settings.TOPIC_NAMES)
    write_events()
    extract_events()
