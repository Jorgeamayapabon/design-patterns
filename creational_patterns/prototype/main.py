from creational_patterns.prototype.config import JobConfig
from creational_patterns.prototype.templates import JobTemplates


def register_templates():
    JobTemplates.register(
        "fast",
        JobConfig(
            name="fast-job",
            retries=1,
            timeout=5,
            metadata={
                "priority": "high"
            }
        )
    )
    JobTemplates.register(
        "safe",
        JobConfig(
            name="safe-job",
            retries=5,
            timeout=30,
            metadata={
                "priority": "low"
            }
        )
    )


def run():
    register_templates()
    job1 = JobTemplates.get("fast")
    job2 = JobTemplates.get("fast")
    job3 = JobTemplates.get("safe")

    job2.metadata["priority"] = "critical"

    print(job1)
    print(job2)
    print(job3)


if __name__ == "__main__":
    run()
