import os
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
NUM_RECORDS = 3000
OUTPUT_DIR = "data/processed"

def generate_compliance_dataset(
    num_records=NUM_RECORDS,
    output_dir=OUTPUT_DIR,
):
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("data/raw/regulations", exist_ok=True)

    frameworks = ["GDPR", "DPDP", "ISO27001", "RBI", "SEBI"]
    requirement_types = [
        "Security of Processing",
        "Access Control",
        "Data Breach Notification",
        "Audit Trail",
        "Governance",
    ]
    control_statuses = ["IMPLEMENTED", "PARTIAL", "NOT_IMPLEMENTED"]
    evidence_statuses = ["AVAILABLE", "PARTIAL", "MISSING"]

    data = []
    for i in range(num_records):
        fw = random.choice(frameworks)
        req_type = random.choice(requirement_types)
        c_status = random.choice(control_statuses)
        e_status = random.choice(evidence_statuses)

        asset_crit = random.randint(1, 5)
        data_sens = random.randint(1, 5)
        hist_inc = random.randint(0, 4)
        biz_impact = random.randint(1, 5)

        deadline = (
            72
            if fw == "GDPR" and random.random() > 0.7
            else 0
        )

        score = asset_crit + data_sens + hist_inc + biz_impact

        # Rule-based risk classification
        if c_status == "NOT_IMPLEMENTED" and e_status == "MISSING" and score >= 12:
            label = "CRITICAL"
        elif c_status == "NOT_IMPLEMENTED" or score >= 11:
            label = "HIGH"
        elif c_status == "PARTIAL" or score >= 8:
            label = "MEDIUM"
        else:
            label = "LOW"

        record = {
            "finding_id": f"F-{i:04d}",
            "framework": fw,
            "requirement_type": req_type,
            "obligation_text": f"Organizations must ensure compliance with {fw} regarding {req_type}.",
            "control_description": f"Control mechanism for {req_type} with status {c_status}.",
            "finding_description": f"Audit finding under {fw}: control status is {c_status} and evidence is {e_status}.",
            "control_status": c_status,
            "evidence_status": e_status,
            "asset_criticality": asset_crit,
            "data_sensitivity": data_sens,
            "historical_incidents": hist_inc,
            "business_impact": biz_impact,
            "regulatory_deadline_hours": deadline,
            "label": label,
        }
        data.append(record)

    df = pd.DataFrame(data)

    # Stratified split supporting both full production size and test sample sizes
    if num_records >= 1500:
        train_df, temp_df = train_test_split(
            df, test_size=1000, stratify=df["label"], random_state=RANDOM_SEED
        )
        val_df, test_df = train_test_split(
            temp_df, test_size=500, stratify=temp_df["label"], random_state=RANDOM_SEED
        )
    else:
        train_df, temp_df = train_test_split(
            df, test_size=0.33, stratify=df["label"], random_state=RANDOM_SEED
        )
        val_df, test_df = train_test_split(
            temp_df, test_size=0.5, stratify=temp_df["label"], random_state=RANDOM_SEED
        )

    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    train_path = os.path.join(output_dir, "train.parquet")
    val_path = os.path.join(output_dir, "val.parquet")
    test_path = os.path.join(output_dir, "test.parquet")

    train_df.to_parquet(train_path, index=False)
    val_df.to_parquet(val_path, index=False)
    test_df.to_parquet(test_path, index=False)

    print(f"Generated {len(df)} compliance findings successfully.")
    return train_df, val_df, test_df

if __name__ == "__main__":
    generate_compliance_dataset()