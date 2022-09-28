import datetime
import json

from cloudevents.conversion import to_structured, to_binary

# NOTE: cloudevents python SDK only currently implements HTTP binding, workaround below
# It would be nice to contribute proper kafka binding support (including tests) to https://github.com/cloudevents/sdk-python
from cloudevents.http import CloudEvent
from event_schemas.apps.advisor.v1.advisor_recommendations import (
    AdvisorRecommendations,
    AdvisorRecommendation,
    RHELSystem,
    RHELSystemTag,
)

from kafka import KafkaProducer, KafkaConsumer

ITERATIONS = 1


def mock_cloudevent_headers():
    return {
        "type": "com.redhat.console.advisor.new-recommendations",
        "source": "urn:redhat:source:console:app:advisor",
        "id": "urn:redhat:console:event:5864ac25-4c52-4c87-bd28-9909a4fa3187",
        "subject": "urn:redhat:subject:console:rhel:08e8ec2b-6a79-4f1d-bea4-a438da139493",
        "time": "2022-09-27T16:08:07.870603Z",
        "schema": "https://console.redhat.com/api/schemas/apps/advisor/v1/advisor-recommendations.json",
        "redhatorgid": "org123",
        "redhatconsolebundle": "rhel",
    }


def mock_advisor_recommendations():
    return AdvisorRecommendations(
        system=RHELSystem(
            display_name="rhel8desktop",
            hostname="rhel8desktop",
            host_url="https://console.redhat.com/insights/inventory/08e8ec2b-6a79-4f1d-bea4-a438da139493",
            rhel_version="8.3",
            inventory_id="08e8ec2b-6a79-4f1d-bea4-a438da139493",
            tags=[
                RHELSystemTag(
                    namespace="insights-client", key="Environment", value="Production"
                )
            ],
        ),
        advisor_recommendations=[
            AdvisorRecommendation(
                publish_date=datetime.datetime.now(),
                reboot_required=False,
                rule_description="System is not able to get the latest recommendations and may miss bug fixes when the Insights Client Core egg file is outdated",
                rule_id="insights_core_egg_not_up2date|INSIGHTS_CORE_EGG_NOT_UP2DATE",
                rule_url="https://console.redhat.com/insights/advisor/recommendations/insights_core_egg_not_up2date|INSIGHTS_CORE_EGG_NOT_UP2DATE/",
                total_risk="2",
            )
        ],
    )


def marshall_data(advisor_recommendations: AdvisorRecommendations):
    return AdvisorRecommendations.to_dict(advisor_recommendations)


def create_event():
    return CloudEvent(mock_cloudevent_headers(), mock_advisor_recommendations())


def produce_binary_message(producer: KafkaProducer):
    # NOTE: the primary difference w/ the http binding is that http binding uses ce- prefix, and kafka uses ce_ prefix
    # See https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/kafka-protocol-binding.md
    # See https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md
    event = create_event()
    headers, body = to_binary(event, data_marshaller=AdvisorRecommendations.to_dict)
    headers = [
        (key.replace("ce-", "ce_"), str(value).encode("utf-8"))
        for key, value in headers.items()
    ]
    headers.append(("content-type", b"application/json"))
    print("Sending binary message")
    producer.send(
        "test-topic",
        headers=headers,
        value=json.dumps(body).encode("utf-8"),
    )


def produce_structured_message(producer: KafkaProducer):
    event = create_event()
    _, body_json = to_structured(event, data_marshaller=AdvisorRecommendations.to_dict)
    print("Sending structured message")
    producer.send(
        "test-topic-structured",
        headers=[("content-type", b"application/cloudevents+json")],
        value=body_json,
    )


def consume_binary_message(consumer: KafkaConsumer):
    print("Waiting for binary message")
    message = next(consumer)
    ce_headers = {
        header[0].replace("ce_", ""): header[1].decode("utf-8")
        for header in message.headers
        if header[0].startswith("ce_")
    }
    data = AdvisorRecommendations.from_dict(json.loads(message.value))
    print(f'Message received for orgId={ce_headers["redhatorgid"]}')
    print(f"Message received for displayName={data.system.display_name}")


def consume_structured_message(consumer: KafkaConsumer):
    print("Waiting for structured message")
    message = next(consumer)
    payload = json.loads(message.value)
    ce_headers = {
        key: value for (key, value) in payload.items() if "key" not in ("data")
    }
    data = AdvisorRecommendations.from_dict(payload["data"])
    print(f'Message received for orgId={ce_headers["redhatorgid"]}')
    print(f"Message received for displayName={data.system.display_name}")


def main():
    producer = KafkaProducer()
    binary_consumer = KafkaConsumer(
        "test-topic", group_id="python-example-binary", auto_offset_reset="earliest"
    )
    structured_consumer = KafkaConsumer(
        "test-topic-structured",
        group_id="python-example-structured",
        auto_offset_reset="earliest",
    )
    for _ in range(ITERATIONS):
        produce_binary_message(producer)
        produce_structured_message(producer)
        consume_binary_message(binary_consumer)
        consume_structured_message(structured_consumer)


if __name__ == "__main__":
    main()
