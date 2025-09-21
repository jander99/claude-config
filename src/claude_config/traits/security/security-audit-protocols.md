---
name: "Security Audit Protocols"
description: "Comprehensive security testing and vulnerability management"
category: "security"
coverage: "OWASP Top 10, vulnerability scanning, penetration testing, security automation"
version: "1.0"
---

## Security Testing Methodologies

### OWASP Top 10 Security Controls
1. **Broken Access Control**: Authorization testing, privilege escalation checks
2. **Cryptographic Failures**: Encryption verification, key management validation
3. **Injection**: SQL injection, NoSQL injection, command injection testing
4. **Insecure Design**: Threat modeling, security architecture review
5. **Security Misconfiguration**: Configuration hardening, default credential checks
6. **Vulnerable Components**: Dependency scanning, third-party security assessment
7. **Authentication Failures**: Multi-factor authentication, session management testing
8. **Software Integrity Failures**: Supply chain security, code signing verification
9. **Logging Failures**: Security event logging, monitoring coverage assessment
10. **Server-Side Request Forgery**: SSRF testing, network boundary validation

### Vulnerability Assessment Framework
```yaml
scanning_categories:
  static_analysis:
    - "SAST: Source code security analysis with SonarQube, Checkmarx, Veracode"
    - "Dependency scanning: Known vulnerability detection in third-party libraries"
    - "License compliance: Open source license compatibility assessment"
    - "Secrets detection: Hardcoded credentials and API key identification"

  dynamic_analysis:
    - "DAST: Running application security testing with OWASP ZAP, Burp Suite"
    - "IAST: Interactive application security testing during runtime"
    - "API security testing: REST/GraphQL endpoint vulnerability assessment"
    - "Authentication testing: Session management and access control validation"

  infrastructure_scanning:
    - "Network scanning: Port enumeration, service fingerprinting"
    - "Configuration assessment: CIS benchmarks, security baseline validation"
    - "Container scanning: Image vulnerability analysis with Twistlock, Aqua"
    - "Cloud security posture: AWS Config, Azure Security Center assessments"
```

### Penetration Testing Methodologies
```yaml
testing_phases:
  reconnaissance:
    - "Information gathering: OSINT, DNS enumeration, subdomain discovery"
    - "Network mapping: Port scanning, service identification, technology stack"
    - "Social engineering assessment: Phishing simulation, physical security"

  vulnerability_identification:
    - "Web application testing: OWASP methodology, business logic flaws"
    - "Network penetration testing: Internal/external network assessment"
    - "Wireless security testing: WiFi security, rogue access point detection"
    - "Mobile application testing: iOS/Android security assessment"

  exploitation:
    - "Proof of concept development: Controlled exploitation demonstration"
    - "Privilege escalation: Local/remote privilege escalation testing"
    - "Post-exploitation: Data access, lateral movement, persistence testing"
    - "Social engineering: Human factor security assessment"

  reporting:
    - "Executive summary: Business impact and risk assessment"
    - "Technical findings: Detailed vulnerability descriptions and remediation"
    - "Proof of concept: Screenshots, code snippets, reproduction steps"
    - "Remediation timeline: Priority-based remediation recommendations"
```

## Security Automation and CI/CD Integration

### Security Pipeline Integration
```yaml
pipeline_security_gates:
  pre_commit:
    - "Git hooks: Secrets scanning, basic syntax validation"
    - "IDE plugins: Real-time security feedback during development"

  continuous_integration:
    - "SAST scanning: Automated source code security analysis"
    - "Dependency scanning: Third-party vulnerability detection"
    - "Container scanning: Base image and dependency vulnerability assessment"
    - "License compliance: Open source license compatibility verification"

  continuous_deployment:
    - "DAST scanning: Automated dynamic security testing in staging"
    - "Infrastructure scanning: Configuration and compliance validation"
    - "Security smoke tests: Critical security control verification"
    - "Penetration testing: Automated security regression testing"
```

### Threat Modeling Framework
```yaml
threat_modeling_methodologies:
  stride_analysis:
    - "Spoofing: Identity verification and authentication controls"
    - "Tampering: Data integrity protection and validation"
    - "Repudiation: Non-repudiation controls and audit logging"
    - "Information Disclosure: Data confidentiality and access controls"
    - "Denial of Service: Availability protection and rate limiting"
    - "Elevation of Privilege: Authorization and privilege management"

  pasta_methodology:
    - "Problem Definition: Security objectives and business requirements"
    - "Attack Simulation: Threat actor modeling and attack path analysis"
    - "Statistical Analysis: Risk quantification and impact assessment"
    - "Threat Analysis: Vulnerability identification and exploit scenarios"
    - "Application Decomposition: Asset identification and data flow mapping"
```

## Security Monitoring and Incident Response

### Security Information and Event Management (SIEM)
```yaml
siem_capabilities:
  log_aggregation:
    - "Centralized logging: Application, system, and security event collection"
    - "Log normalization: Standardized event format and correlation"
    - "Real-time analysis: Immediate threat detection and alerting"

  threat_detection:
    - "Rule-based detection: Known attack pattern identification"
    - "Behavioral analysis: Anomaly detection and baseline deviation"
    - "Threat intelligence: IOC matching and attribution analysis"
    - "Machine learning: Advanced threat detection and false positive reduction"
```

### Incident Response Procedures
```yaml
incident_classification:
  severity_1_critical:
    - "Active data breach with confirmed data exfiltration"
    - "Complete system compromise with administrative access"
    - "Ransomware attack with system encryption"
    - "Response time: Immediate (within 15 minutes)"

  severity_2_high:
    - "Unauthorized access to sensitive systems or data"
    - "Malware infection with potential for lateral movement"
    - "DDoS attack affecting system availability"
    - "Response time: Within 1 hour"

  severity_3_medium:
    - "Failed intrusion attempts with no system compromise"
    - "Policy violations with potential security impact"
    - "Suspicious network activity requiring investigation"
    - "Response time: Within 4 hours"
```

## Security Compliance and Audit Preparation

### Security Control Validation
- [ ] Multi-factor authentication enforced for privileged access
- [ ] Encryption at rest and in transit implemented with proper key management
- [ ] Input validation and output encoding implemented consistently
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Regular vulnerability assessments and penetration testing completed
- [ ] Security incident response procedures tested and documented
- [ ] Security awareness training completed for all personnel
- [ ] Third-party security assessments and vendor risk evaluations current

### Audit Documentation Requirements
- [ ] Security policies and procedures documented and approved
- [ ] Risk assessments completed with mitigation strategies
- [ ] Security control testing evidence collected and maintained
- [ ] Incident response logs and lessons learned documented
- [ ] Compliance mapping to regulatory requirements maintained
- [ ] Security metrics and KPIs tracked and reported
- [ ] Continuous monitoring evidence collected and analyzed
- [ ] Security training records and certifications maintained