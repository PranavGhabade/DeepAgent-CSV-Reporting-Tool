# Dataset Analysis Report

## Executive Summary

This report provides a comprehensive security and traffic analysis of Palo Alto Firewall logs captured over a 20-minute window on June 6, 2025, between 11:50:10 and 12:10:00. The dataset consists of 84,550 rows and 61 columns from a Palo Alto PA-440 firewall device operating under the virtual system vsys1. The primary objective of this analysis is to evaluate network traffic patterns, assess security policy enforcement, and identify potential threat vectors within the network.

The analysis reveals that while the vast majority of the traffic was allowed (79,518 events), there are critical security and data quality concerns. Specifically, the firewall logged 34 suspicious Command and Control (C2C) communication attempts targeting an internal host (192.168.28.59) from an external malicious IP (103.10.24.44). Furthermore, exactly 50% of the dataset (42,225 rows) consists of duplicate records, indicating significant inefficiencies in the log collection and ingestion pipeline.

## Dataset Overview

• Number of rows: 84,550

• Number of columns: 61

• Data types: 19 numeric columns, 36 categorical columns, and 5 datetime columns

• Missing values: Threat-related columns (`_threat_category`, `_threat_family_name`, `_threat_ioc`, `_threat_malware_ip`, `_threat_source`, `_threat_type`, `_threat_victim_ip`) have 84,516 missing values (99.96%). The `outbound_if` column has 4,990 missing values (5.9%).

• Duplicate rows: 42,225 duplicate rows (50.0% of the dataset)

• Dataset quality: The dataset quality is heavily impacted by the 50% duplication rate, which artificially inflates traffic metrics. Additionally, threat intelligence fields are 99.96% empty, limiting the depth of threat context. However, the matching count of missing `outbound_if` values with "deny" actions (4,990 events) shows logical consistency in firewall logging.

## Statistical Findings

The statistical analysis of the firewall logs highlights key operational metrics and traffic behaviors across the network.

### Table 1. Key Traffic Metrics Summary

| Metric | Mean | Minimum | Maximum | Standard Deviation |
| :--- | :--- | :--- | :--- | :--- |
| Bytes Received | 30,977.90 | 0.0 | 104,054,808.0 | 1,088,820.12 |
| Bytes Sent | 5,712.05 | 60.0 | 54,619,888.0 | 357,447.56 |
| Total Bytes | 36,689.95 | 60.0 | 104,365,342.0 | 1,184,440.31 |
| Elapsed Time (seconds) | 14.32 | 0.0 | 8,455.0 | 135.98 |
| Risk Level | 2.54 | 1.0 | 5.0 | 1.10 |

### Table 2. Top Categorical Distributions

| Column | Top Value | Frequency | Percentage of Total |
| :--- | :--- | :--- | :--- |
| Action | allow | 79,518 | 94.05% |
| App Category | networking | 61,661 | 72.93% |
| Application | dns-base | 38,076 | 45.03% |
| Protocol | udp | 52,420 | 62.00% |
| Rule Name | Allow-any | 63,321 | 74.89% |
| Source Country | United States | 61,175 | 72.35% |

The average risk level of the traffic is 2.54 out of 5, indicating moderate risk overall. There is an extremely strong positive correlation between `bytes_received` and `total_bytes` (0.954), as well as between `bytes_received` and `pkts_received` (0.833), indicating that inbound traffic dominates the total bandwidth consumption. A moderate positive correlation of 0.627 exists between `destport` and `nat_dest_port`. 

Conversely, a weak negative correlation of -0.334 exists between `destport` and `srcport`. A massive number of outliers exist in network volume metrics, such as 18,334 outliers in `pkts_received` and 15,735 in `bytes_received`, pointing to bursty traffic or specific high-volume sessions.

## Visual Analysis

### Figure 1. Total Bytes Over Time

Description
This line chart displays the trend of total bytes transmitted across the network over the logged timestamps from 11:50:10 to 12:10:00 on June 6, 2025.

Analysis
The chart highlights network activity fluctuations over the 20-minute window, showing specific peaks in data volume that correspond to high-bandwidth sessions or periodic network events.

### Figure 2. Distribution of Firewall Actions

Description
This pie chart illustrates the proportion of different actions taken by the firewall, specifically comparing allowed, denied, and reset-both traffic events.

Analysis
The visualization emphasizes that the vast majority of traffic is allowed (79,518 events), while a small fraction is denied (4,990 events) or reset (42 events), showing that standard operations dominate the log volume.

### Figure 3. Total Bytes by Application Category

Description
This bar chart represents the total bytes consumed across different application categories, such as networking, unknown, general-internet, saas, and collaboration.

Analysis
The chart demonstrates which application categories are responsible for the bulk of the network bandwidth, with networking and unknown categories driving the highest data transfer volumes.

### Figure 4. Total Bytes by Source Country

Description
This bar chart shows the total bytes transferred originating from different source countries, including the United States, India, Australia, and others.

Analysis
The visualization confirms that the United States is not only the top source by event count (61,175 events) but also a major contributor to total network bandwidth, followed by other key regions like India and Australia.

### Figure 5. Bytes Sent vs. Bytes Received

Description
This scatter plot maps the relationship between bytes sent and bytes received for individual network sessions.

Analysis
The plot reveals the distribution of data exchange patterns, showing that most sessions involve low data transfer, while a few extreme outliers represent massive asymmetric downloads (high bytes received) or uploads (high bytes sent).

## Business Insights

### Important Patterns

• UDP is the dominant protocol, accounting for 52,420 events, primarily driven by dns-base applications (38,076 events).

• The United States is the primary geographic source of traffic, representing 61,175 of the total 84,550 events.

• The "Allow-any" firewall rule is heavily relied upon, triggering 63,321 times and representing the vast majority of allowed traffic.

### Trends

• Network traffic is highly asymmetric, with a strong correlation (0.833) between bytes received and packets received, indicating that the network primarily downloads data rather than uploading.

• Traffic is concentrated in a very short 20-minute window, showing rapid, high-frequency connection attempts.

### Risks

• Active Command and Control (C2C) threat activity was detected, with 34 suspicious events involving external IP 103.10.24.44 targeting internal host 192.168.28.59.

• Over-reliance on the broad "Allow-any" rule (63,321 events) exposes the organization to unauthorized lateral movement or data exfiltration.

• Severe log duplication (50% of the dataset) compromises data integrity and inflates storage and processing costs.

### Opportunities

• Optimizing firewall rules by replacing "Allow-any" with application-specific rules can significantly improve the organization's security posture.

• Streamlining the log ingestion pipeline to eliminate duplicate records will reduce SIEM storage costs and improve analytical accuracy.

## Recommendations

• Isolate and conduct an immediate forensic investigation on the internal host at IP 192.168.28.59 to check for compromise or malware infection due to the 34 flagged Command and Control (C2C) events.

• Implement an explicit firewall block rule to deny all traffic to and from the external malicious IP address 103.10.24.44.

• Audit and deprecate the broad "Allow-any" firewall rule, replacing it with strict, port-specific, and application-specific rules to enforce a least-privilege access model.

• Troubleshoot and reconfigure the Syslog forwarding or ingestion pipeline to resolve the 50% log duplication issue (42,225 duplicate rows).

• Configure automated alerts for any traffic categorized under the "[Suspicious]" threat category or "[Suspicious_C2C]" threat family to enable real-time incident response.

## Conclusion

In conclusion, the analysis of the Palo Alto PA-440 firewall logs reveals a network that is highly active but exposed to notable security and operational risks. While standard networking and DNS traffic dominate the allowed connections, the detection of 34 active Command and Control communication attempts targeting an internal host demands immediate remediation. Addressing these security gaps by tightening firewall rules, isolating the targeted host, and fixing the 50% log duplication issue will significantly enhance both the security posture and operational efficiency of the organization.