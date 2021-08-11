package com.kkennib.kafka;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.apache.maven.shared.utils.StringUtils;

import java.time.Duration;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Properties;

public class KafakaConsumer {

    public void consume(String topic) {
        Properties config = new Properties();
        config.put("bootstrap.servers", "localhost:9092");
        config.put("session.timeout.ms", "10000");
        config.put("group.id", topic);
        config.put("enable.auto.commit", "true");
        config.put("auto.offset.reset", "latest");
        config.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        config.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(config);
        TopicPartition topicPartition = new TopicPartition(topic, 0);
        List<TopicPartition> partitionList = Arrays.asList(topicPartition);
        consumer.assign(partitionList);
        consumer.seekToBeginning(partitionList);

        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            System.out.println(record.value());
        }
    }

}
