from config import settings, consumer_config
from extractor import KafkaExtractor
from pre_start import create_kafka_topics


def extract_events():
    # для проверки работоспособности
    extractor = KafkaExtractor(settings.TOPIC_NAMES, consumer_config)
    for key, value in extractor.fetch():
        print(f"Message consumed: key = {key} value = {value}")


if __name__ == "__main__":
    from _producer import write_events

    create_kafka_topics(settings.TOPIC_NAMES)
    write_events()
    extract_events()
