"""
Security and Compliance Standards Integration

Comprehensive integration of OWASP, NIST, ISO 27001, and other security standards
with automated compliance checking and implementation guidance generation.
"""

import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ComplianceFramework(Enum):
    """Supported compliance frameworks"""
    OWASP_TOP_10 = "owasp_top_10"
    OWASP_API_SECURITY = "owasp_api_security"
    OWASP_MOBILE = "owasp_mobile"
    NIST_CSF = "nist_cybersecurity_framework"
    NIST_PRIVACY = "nist_privacy_framework"
    NIST_SSDF = "nist_secure_software_development"
    ISO_27001 = "iso_27001"
    ISO_27017 = "iso_27017_cloud"
    ISO_27018 = "iso_27018_privacy"
    SOC2_TYPE2 = "soc2_type2"
    GDPR = "gdpr_compliance"
    HIPAA = "hipaa_security_rule"
    PCI_DSS = "pci_dss"


class SecurityDomain(Enum):
    """Security domains for classification"""
    WEB_APPLICATION = "web_application"
    API_SECURITY = "api_security"
    MOBILE_SECURITY = "mobile_security"
    CLOUD_SECURITY = "cloud_security"
    DATA_PROTECTION = "data_protection"
    IDENTITY_ACCESS = "identity_access_management"
    NETWORK_SECURITY = "network_security"
    ENDPOINT_SECURITY = "endpoint_security"
    INCIDENT_RESPONSE = "incident_response"
    GOVERNANCE_RISK = "governance_risk_compliance"


@dataclass
class SecurityControl:
    """Individual security control or requirement"""
    id: str
    title: str
    description: str
    framework: ComplianceFramework
    domain: SecurityDomain
    severity: str  # 'critical', 'high', 'medium', 'low'
    implementation_guidance: str
    verification_criteria: List[str]
    related_controls: List[str] = field(default_factory=list)
    applicable_technologies: List[str] = field(default_factory=list)
    compliance_evidence: Optional[str] = None
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ComplianceAssessment:
    """Compliance assessment for a specific framework and technology stack"""
    framework: ComplianceFramework
    technology_stack: List[str]
    assessment_date: datetime
    overall_score: float  # 0-100
    control_results: Dict[str, Dict[str, Any]]  # control_id -> {status, evidence, recommendations}
    recommendations: List[str]
    next_review_date: datetime
    assessor: str = "automated"


@dataclass
class SecurityStandard:
    """Complete security standard with all controls"""
    framework: ComplianceFramework
    version: str
    publication_date: datetime
    controls: Dict[str, SecurityControl]
    metadata: Dict[str, Any] = field(default_factory=dict)


class SecurityComplianceProvider:
    """
    Comprehensive security and compliance standards provider with automated
    assessment capabilities and implementation guidance generation.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.security_standards: Dict[ComplianceFramework, SecurityStandard] = {}
        self.assessment_cache: Dict[str, ComplianceAssessment] = {}

        # Initialize security standards
        asyncio.create_task(self._initialize_security_standards())

        # Start background update tasks
        asyncio.create_task(self._standards_update_loop())

    def _default_config(self) -> Dict:
        """Default configuration for security compliance provider"""
        return {
            'standards': {
                'update_frequency_days': 30,
                'cache_ttl_hours': 24,
                'min_compliance_score': 85.0,
                'assessment_validity_days': 90
            },
            'severity_scoring': {
                'critical': 25.0,
                'high': 15.0,
                'medium': 8.0,
                'low': 2.0
            },
            'technology_mappings': {
                'web_frameworks': ['django', 'fastapi', 'react', 'angular', 'vue'],
                'mobile_frameworks': ['react-native', 'flutter', 'ionic'],
                'cloud_platforms': ['aws', 'azure', 'gcp'],
                'databases': ['postgresql', 'mysql', 'mongodb', 'redis']
            }
        }

    async def _initialize_security_standards(self):
        """Initialize all supported security standards"""
        logger.info("Initializing security and compliance standards")

        # Initialize OWASP standards
        await self._initialize_owasp_standards()

        # Initialize NIST standards
        await self._initialize_nist_standards()

        # Initialize ISO standards
        await self._initialize_iso_standards()

        # Initialize other compliance frameworks
        await self._initialize_other_frameworks()

        logger.info(f"Initialized {len(self.security_standards)} security standards")

    async def _initialize_owasp_standards(self):
        """Initialize OWASP security standards"""

        # OWASP Top 10 Web Application Security Risks (2021)
        owasp_top_10_controls = {
            'A01_2021': SecurityControl(
                id='A01_2021',
                title='Broken Access Control',
                description='Access control enforces policy such that users cannot act outside of their intended permissions',
                framework=ComplianceFramework.OWASP_TOP_10,
                domain=SecurityDomain.IDENTITY_ACCESS,
                severity='critical',
                implementation_guidance='''
                Implementation Guidance for Broken Access Control:

                1. **Deny by Default**: Implement deny by default access controls
                2. **Principle of Least Privilege**: Grant minimum necessary permissions
                3. **Access Control Mechanisms**:
                   - Role-Based Access Control (RBAC)
                   - Attribute-Based Access Control (ABAC)
                   - Mandatory Access Control where appropriate

                4. **Technical Controls**:
                   ```python
                   # Example: Django permission decorators
                   from django.contrib.auth.decorators import login_required, permission_required

                   @login_required
                   @permission_required('app.view_sensitive_data')
                   def sensitive_view(request):
                       # Only authenticated users with proper permission can access
                       pass
                   ```

                5. **Verification Steps**:
                   - Log access control failures and alert admins
                   - Rate limit API and controller access
                   - Implement proper session management
                   - Validate JWT tokens and disable them after logout
                ''',
                verification_criteria=[
                    'Access controls implemented at application layer',
                    'Default deny policy in place',
                    'Session management properly implemented',
                    'Access control failures logged and monitored',
                    'Rate limiting implemented for sensitive endpoints'
                ],
                applicable_technologies=['django', 'fastapi', 'react', 'angular', 'vue', 'spring-boot']
            ),

            'A02_2021': SecurityControl(
                id='A02_2021',
                title='Cryptographic Failures',
                description='Protect data in transit and at rest using strong cryptographic controls',
                framework=ComplianceFramework.OWASP_TOP_10,
                domain=SecurityDomain.DATA_PROTECTION,
                severity='critical',
                implementation_guidance='''
                Implementation Guidance for Cryptographic Failures:

                1. **Data Classification**: Classify data requiring protection
                2. **Encryption in Transit**:
                   - Use TLS 1.2+ for all data transmission
                   - Implement HTTP Strict Transport Security (HSTS)
                   - Use proper certificate validation

                3. **Encryption at Rest**:
                   ```python
                   # Example: Django encrypted field
                   from django_cryptography.fields import encrypt

                   class UserProfile(models.Model):
                       ssn = encrypt(models.CharField(max_length=11))
                   ```

                4. **Key Management**:
                   - Use hardware security modules (HSM) for key storage
                   - Implement proper key rotation policies
                   - Never store keys in code or configuration files

                5. **Cryptographic Standards**:
                   - Use approved algorithms (AES-256, RSA-2048+)
                   - Avoid deprecated algorithms (MD5, SHA1, DES)
                   - Use cryptographically secure random number generators
                ''',
                verification_criteria=[
                    'TLS 1.2+ implemented for all data transmission',
                    'Sensitive data encrypted at rest',
                    'Strong cryptographic algorithms used',
                    'Proper key management implemented',
                    'No hardcoded cryptographic keys'
                ],
                applicable_technologies=['all']
            ),

            'A03_2021': SecurityControl(
                id='A03_2021',
                title='Injection',
                description='Prevent injection flaws such as SQL, NoSQL, OS, and LDAP injection',
                framework=ComplianceFramework.OWASP_TOP_10,
                domain=SecurityDomain.WEB_APPLICATION,
                severity='critical',
                implementation_guidance='''
                Implementation Guidance for Injection Prevention:

                1. **Input Validation**:
                   - Validate all input using positive validation
                   - Use allow-lists over deny-lists
                   - Validate input length, character sets, and format

                2. **Parameterized Queries**:
                   ```python
                   # Secure: Using parameterized queries
                   cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

                   # Insecure: String concatenation
                   cursor.execute("SELECT * FROM users WHERE id = " + user_id)
                   ```

                3. **ORM Usage**:
                   ```python
                   # Django ORM automatically prevents SQL injection
                   User.objects.filter(username=user_input)
                   ```

                4. **Output Encoding**:
                   - Encode output based on context (HTML, URL, CSS, JavaScript)
                   - Use templating engines with auto-escaping

                5. **Command Injection Prevention**:
                   - Avoid system calls with user input
                   - Use APIs instead of shell commands
                   - Validate and sanitize all inputs to external systems
                ''',
                verification_criteria=[
                    'Parameterized queries used for all database access',
                    'Input validation implemented for all user inputs',
                    'Output encoding applied based on context',
                    'No dynamic query construction with user input',
                    'System command usage avoided or properly sanitized'
                ],
                applicable_technologies=['django', 'fastapi', 'spring-boot', 'express', 'postgresql', 'mysql']
            )
        }

        # OWASP API Security Top 10
        owasp_api_controls = {
            'API1_2023': SecurityControl(
                id='API1_2023',
                title='Broken Object Level Authorization',
                description='Ensure users can only access objects they have permission to access',
                framework=ComplianceFramework.OWASP_API_SECURITY,
                domain=SecurityDomain.API_SECURITY,
                severity='critical',
                implementation_guidance='''
                API Object Level Authorization Implementation:

                1. **Authorization Checks**:
                   ```python
                   # FastAPI example with dependency injection
                   from fastapi import Depends, HTTPException

                   async def verify_object_access(
                       object_id: int,
                       current_user: User = Depends(get_current_user)
                   ):
                       if not user_can_access_object(current_user, object_id):
                           raise HTTPException(status_code=403, detail="Access denied")
                       return object_id

                   @app.get("/api/objects/{object_id}")
                   async def get_object(
                       object_id: int = Depends(verify_object_access)
                   ):
                       return get_object_by_id(object_id)
                   ```

                2. **Policy Enforcement Points**:
                   - Implement authorization at every API endpoint
                   - Use consistent authorization mechanisms
                   - Avoid relying on client-side authorization
                ''',
                verification_criteria=[
                    'Authorization implemented at every API endpoint',
                    'Object-level access controls verified',
                    'User permissions validated for each request',
                    'Authorization decisions logged'
                ],
                applicable_technologies=['fastapi', 'django-rest-framework', 'express', 'spring-boot']
            )
        }

        self.security_standards[ComplianceFramework.OWASP_TOP_10] = SecurityStandard(
            framework=ComplianceFramework.OWASP_TOP_10,
            version='2021',
            publication_date=datetime(2021, 9, 24),
            controls=owasp_top_10_controls
        )

        self.security_standards[ComplianceFramework.OWASP_API_SECURITY] = SecurityStandard(
            framework=ComplianceFramework.OWASP_API_SECURITY,
            version='2023',
            publication_date=datetime(2023, 7, 25),
            controls=owasp_api_controls
        )

    async def _initialize_nist_standards(self):
        """Initialize NIST security standards"""

        nist_csf_controls = {
            'ID.AM-1': SecurityControl(
                id='ID.AM-1',
                title='Physical devices and systems within the organization are inventoried',
                description='Maintain accurate inventory of physical devices and systems',
                framework=ComplianceFramework.NIST_CSF,
                domain=SecurityDomain.GOVERNANCE_RISK,
                severity='medium',
                implementation_guidance='''
                NIST CSF Identify - Asset Management Implementation:

                1. **Asset Inventory**:
                   - Maintain comprehensive asset database
                   - Include hardware, software, and data assets
                   - Regular asset discovery and validation

                2. **Asset Classification**:
                   - Classify assets by criticality and sensitivity
                   - Implement asset labeling and tracking
                   - Document asset ownership and responsibilities

                3. **Automated Discovery**:
                   ```bash
                   # Example: Network asset discovery
                   nmap -sP 192.168.1.0/24
                   # Integrate with CMDB systems
                   ```
                ''',
                verification_criteria=[
                    'Complete asset inventory maintained',
                    'Assets classified by criticality',
                    'Regular asset discovery performed',
                    'Asset ownership documented'
                ],
                applicable_technologies=['network-security', 'enterprise-tools']
            ),

            'PR.AC-1': SecurityControl(
                id='PR.AC-1',
                title='Identities and credentials are issued, managed, verified, revoked, and audited',
                description='Comprehensive identity and credential lifecycle management',
                framework=ComplianceFramework.NIST_CSF,
                domain=SecurityDomain.IDENTITY_ACCESS,
                severity='high',
                implementation_guidance='''
                NIST CSF Protect - Access Control Implementation:

                1. **Identity Lifecycle Management**:
                   - Automated user provisioning and deprovisioning
                   - Regular access reviews and certifications
                   - Multi-factor authentication for privileged accounts

                2. **Technical Implementation**:
                   ```python
                   # Example: Django user management
                   from django.contrib.auth.models import User
                   from django.contrib.auth import authenticate

                   def provision_user(username, email, groups):
                       user = User.objects.create_user(username=username, email=email)
                       for group in groups:
                           user.groups.add(group)
                       return user
                   ```

                3. **Credential Management**:
                   - Strong password policies
                   - Regular credential rotation
                   - Secure credential storage
                ''',
                verification_criteria=[
                    'Identity lifecycle processes documented',
                    'Multi-factor authentication implemented',
                    'Regular access reviews conducted',
                    'Credential management policies enforced'
                ],
                applicable_technologies=['django', 'fastapi', 'spring-security', 'active-directory']
            )
        }

        self.security_standards[ComplianceFramework.NIST_CSF] = SecurityStandard(
            framework=ComplianceFramework.NIST_CSF,
            version='1.1',
            publication_date=datetime(2018, 4, 16),
            controls=nist_csf_controls
        )

    async def _initialize_iso_standards(self):
        """Initialize ISO 27001 security standards"""

        iso_27001_controls = {
            'A.5.1.1': SecurityControl(
                id='A.5.1.1',
                title='Policies for information security',
                description='Set of policies for information security shall be defined',
                framework=ComplianceFramework.ISO_27001,
                domain=SecurityDomain.GOVERNANCE_RISK,
                severity='high',
                implementation_guidance='''
                ISO 27001 Information Security Policy Implementation:

                1. **Policy Development**:
                   - Develop comprehensive information security policy
                   - Align with business objectives and regulatory requirements
                   - Regular review and approval by management

                2. **Policy Components**:
                   - Information security objectives
                   - Risk management approach
                   - Roles and responsibilities
                   - Compliance requirements

                3. **Implementation**:
                   - Communicate policies to all personnel
                   - Provide security awareness training
                   - Monitor policy compliance
                ''',
                verification_criteria=[
                    'Information security policy documented',
                    'Policy approved by management',
                    'Policy communicated to all staff',
                    'Regular policy reviews conducted'
                ],
                applicable_technologies=['governance-tools', 'policy-management']
            ),

            'A.9.1.2': SecurityControl(
                id='A.9.1.2',
                title='Access to networks and network services',
                description='Users shall only be provided with access to network services',
                framework=ComplianceFramework.ISO_27001,
                domain=SecurityDomain.NETWORK_SECURITY,
                severity='high',
                implementation_guidance='''
                ISO 27001 Network Access Control Implementation:

                1. **Network Segmentation**:
                   - Implement network zones and DMZ
                   - Use firewalls to control traffic flow
                   - Separate production from development networks

                2. **Access Control**:
                   ```bash
                   # Example: iptables firewall rules
                   iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT
                   iptables -A INPUT -p tcp --dport 22 -j DROP
                   ```

                3. **Network Monitoring**:
                   - Implement intrusion detection systems
                   - Monitor network traffic for anomalies
                   - Log and audit network access
                ''',
                verification_criteria=[
                    'Network access controls implemented',
                    'Network segmentation in place',
                    'Access to network services restricted',
                    'Network activity monitored and logged'
                ],
                applicable_technologies=['network-security', 'firewalls', 'ids-ips']
            )
        }

        self.security_standards[ComplianceFramework.ISO_27001] = SecurityStandard(
            framework=ComplianceFramework.ISO_27001,
            version='2022',
            publication_date=datetime(2022, 10, 25),
            controls=iso_27001_controls
        )

    async def _initialize_other_frameworks(self):
        """Initialize other compliance frameworks (SOC2, GDPR, etc.)"""

        # SOC 2 Type II Controls
        soc2_controls = {
            'CC6.1': SecurityControl(
                id='CC6.1',
                title='Logical and Physical Access Controls',
                description='Restrict logical and physical access to system resources',
                framework=ComplianceFramework.SOC2_TYPE2,
                domain=SecurityDomain.IDENTITY_ACCESS,
                severity='high',
                implementation_guidance='''
                SOC 2 Logical and Physical Access Controls:

                1. **Logical Access Controls**:
                   - Multi-factor authentication for all users
                   - Role-based access control (RBAC)
                   - Regular access reviews and certifications

                2. **Physical Access Controls**:
                   - Secure data center facilities
                   - Badge-controlled access to server rooms
                   - Visitor management procedures

                3. **Technical Implementation**:
                   ```python
                   # Example: MFA implementation
                   from django_otp.decorators import otp_required

                   @otp_required
                   def sensitive_operation(request):
                       # This view requires MFA
                       pass
                   ```
                ''',
                verification_criteria=[
                    'Multi-factor authentication implemented',
                    'Role-based access control in place',
                    'Physical access controls documented',
                    'Regular access reviews conducted'
                ],
                applicable_technologies=['django', 'fastapi', 'active-directory', 'okta']
            )
        }

        # GDPR Compliance Controls
        gdpr_controls = {
            'Art25': SecurityControl(
                id='Art25',
                title='Data Protection by Design and by Default',
                description='Implement appropriate technical and organizational measures',
                framework=ComplianceFramework.GDPR,
                domain=SecurityDomain.DATA_PROTECTION,
                severity='critical',
                implementation_guidance='''
                GDPR Data Protection by Design Implementation:

                1. **Privacy by Design Principles**:
                   - Minimize data collection and processing
                   - Implement purpose limitation
                   - Ensure data accuracy and storage limitation

                2. **Technical Measures**:
                   ```python
                   # Example: Data anonymization
                   import hashlib

                   def anonymize_email(email):
                       return hashlib.sha256(email.encode()).hexdigest()[:16]

                   # Example: Data retention policy
                   from datetime import datetime, timedelta

                   def cleanup_old_data():
                       cutoff_date = datetime.now() - timedelta(days=365*2)
                       OldData.objects.filter(created_at__lt=cutoff_date).delete()
                   ```

                3. **Organizational Measures**:
                   - Conduct privacy impact assessments
                   - Implement data breach notification procedures
                   - Provide data subject rights mechanisms
                ''',
                verification_criteria=[
                    'Privacy impact assessments conducted',
                    'Data minimization principles applied',
                    'Data subject rights implemented',
                    'Breach notification procedures in place'
                ],
                applicable_technologies=['django', 'fastapi', 'data-processing-tools']
            )
        }

        self.security_standards[ComplianceFramework.SOC2_TYPE2] = SecurityStandard(
            framework=ComplianceFramework.SOC2_TYPE2,
            version='2017',
            publication_date=datetime(2017, 5, 1),
            controls=soc2_controls
        )

        self.security_standards[ComplianceFramework.GDPR] = SecurityStandard(
            framework=ComplianceFramework.GDPR,
            version='2018',
            publication_date=datetime(2018, 5, 25),
            controls=gdpr_controls
        )

    async def get_compliance_requirements(self,
                                        frameworks: List[ComplianceFramework],
                                        technology_stack: List[str],
                                        domain: Optional[SecurityDomain] = None) -> Dict[str, List[SecurityControl]]:
        """
        Get compliance requirements for specific frameworks and technology stack
        """
        requirements = {}

        for framework in frameworks:
            if framework not in self.security_standards:
                logger.warning(f"Framework {framework} not available")
                continue

            standard = self.security_standards[framework]
            applicable_controls = []

            for control in standard.controls.values():
                # Filter by domain if specified
                if domain and control.domain != domain:
                    continue

                # Filter by technology stack
                if self._is_control_applicable(control, technology_stack):
                    applicable_controls.append(control)

            requirements[framework.value] = applicable_controls

        return requirements

    async def assess_compliance(self,
                              framework: ComplianceFramework,
                              technology_stack: List[str],
                              current_implementations: Dict[str, Dict[str, Any]]) -> ComplianceAssessment:
        """
        Assess compliance against a specific framework
        """
        assessment_key = f"{framework.value}:{':'.join(sorted(technology_stack))}"

        # Check cache first
        if (assessment_key in self.assessment_cache and
            (datetime.now() - self.assessment_cache[assessment_key].assessment_date).days <
            self.config['standards']['assessment_validity_days']):
            return self.assessment_cache[assessment_key]

        if framework not in self.security_standards:
            raise ValueError(f"Framework {framework} not available")

        standard = self.security_standards[framework]
        control_results = {}
        total_score = 0.0
        max_possible_score = 0.0

        for control_id, control in standard.controls.items():
            if not self._is_control_applicable(control, technology_stack):
                continue

            # Assess individual control
            control_result = await self._assess_control(control, current_implementations.get(control_id, {}))
            control_results[control_id] = control_result

            # Calculate scoring
            severity_weight = self.config['severity_scoring'][control.severity]
            max_possible_score += severity_weight

            if control_result['status'] == 'compliant':
                total_score += severity_weight
            elif control_result['status'] == 'partially_compliant':
                total_score += severity_weight * 0.5

        # Calculate overall score
        overall_score = (total_score / max_possible_score * 100) if max_possible_score > 0 else 0

        # Generate recommendations
        recommendations = self._generate_compliance_recommendations(control_results, technology_stack)

        # Create assessment
        assessment = ComplianceAssessment(
            framework=framework,
            technology_stack=technology_stack,
            assessment_date=datetime.now(),
            overall_score=overall_score,
            control_results=control_results,
            recommendations=recommendations,
            next_review_date=datetime.now() + timedelta(days=self.config['standards']['assessment_validity_days'])
        )

        # Cache assessment
        self.assessment_cache[assessment_key] = assessment

        return assessment

    async def generate_implementation_guide(self,
                                          framework: ComplianceFramework,
                                          technology_stack: List[str],
                                          priority: str = 'high') -> str:
        """
        Generate implementation guide for specific framework and technology stack
        """
        if framework not in self.security_standards:
            raise ValueError(f"Framework {framework} not available")

        standard = self.security_standards[framework]
        applicable_controls = [
            control for control in standard.controls.values()
            if (self._is_control_applicable(control, technology_stack) and
                (priority == 'all' or control.severity in ['critical', 'high'] if priority == 'high' else True))
        ]

        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        applicable_controls.sort(key=lambda x: severity_order.get(x.severity, 4))

        guide = f"""
# {framework.value.upper()} Implementation Guide

**Technology Stack**: {', '.join(technology_stack)}
**Priority Level**: {priority.title()}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This guide provides implementation guidance for {len(applicable_controls)} security controls
from the {framework.value.upper()} framework, specifically tailored for your technology stack.

## Implementation Roadmap

"""

        for i, control in enumerate(applicable_controls, 1):
            guide += f"""
### {i}. {control.title} ({control.id})

**Severity**: {control.severity.upper()}
**Domain**: {control.domain.value.replace('_', ' ').title()}

**Description**: {control.description}

{control.implementation_guidance}

**Verification Criteria**:
{chr(10).join(f'- {criterion}' for criterion in control.verification_criteria)}

**Applicable Technologies**: {', '.join(control.applicable_technologies)}

---

"""

        guide += f"""
## Implementation Priority Matrix

| Priority | Severity | Controls | Recommended Timeline |
|----------|----------|----------|---------------------|
| 1 | Critical | {len([c for c in applicable_controls if c.severity == 'critical'])} | 0-30 days |
| 2 | High | {len([c for c in applicable_controls if c.severity == 'high'])} | 30-90 days |
| 3 | Medium | {len([c for c in applicable_controls if c.severity == 'medium'])} | 90-180 days |
| 4 | Low | {len([c for c in applicable_controls if c.severity == 'low'])} | 180+ days |

## Next Steps

1. Review and prioritize controls based on your organization's risk tolerance
2. Assign implementation owners for each control
3. Develop detailed implementation plans with timelines
4. Implement monitoring and validation procedures
5. Schedule regular compliance assessments

---

*This guide was generated automatically by the Claude Config Security Compliance Provider*
"""

        return guide

    def _is_control_applicable(self, control: SecurityControl, technology_stack: List[str]) -> bool:
        """Check if a security control is applicable to the technology stack"""
        if 'all' in control.applicable_technologies:
            return True

        # Check for exact matches
        for tech in technology_stack:
            if tech.lower() in [t.lower() for t in control.applicable_technologies]:
                return True

        # Check for category matches
        tech_categories = self.config['technology_mappings']
        for category, technologies in tech_categories.items():
            if any(tech.lower() in [t.lower() for t in technologies] for tech in technology_stack):
                if category in control.applicable_technologies:
                    return True

        return False

    async def _assess_control(self, control: SecurityControl,
                            current_implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance status of an individual control"""

        # Default assessment result
        result = {
            'status': 'not_implemented',  # 'compliant', 'partially_compliant', 'not_implemented'
            'score': 0.0,
            'evidence': [],
            'gaps': [],
            'recommendations': []
        }

        # Check if implementation information is provided
        if not current_implementation:
            result['gaps'] = control.verification_criteria
            result['recommendations'] = [f"Implement {control.title}"]
            return result

        # Assess against verification criteria
        implemented_criteria = 0
        total_criteria = len(control.verification_criteria)

        for criterion in control.verification_criteria:
            criterion_key = criterion.lower().replace(' ', '_')
            if current_implementation.get(criterion_key, False):
                implemented_criteria += 1
                result['evidence'].append(f"✓ {criterion}")
            else:
                result['gaps'].append(f"✗ {criterion}")

        # Calculate compliance score
        compliance_ratio = implemented_criteria / total_criteria if total_criteria > 0 else 0
        result['score'] = compliance_ratio * 100

        # Determine status
        if compliance_ratio >= 0.9:
            result['status'] = 'compliant'
        elif compliance_ratio >= 0.5:
            result['status'] = 'partially_compliant'
        else:
            result['status'] = 'not_implemented'

        # Generate recommendations for gaps
        if result['gaps']:
            result['recommendations'] = [
                f"Address gap: {gap.replace('✗ ', '')}" for gap in result['gaps']
            ]

        return result

    def _generate_compliance_recommendations(self,
                                           control_results: Dict[str, Dict[str, Any]],
                                           technology_stack: List[str]) -> List[str]:
        """Generate overall compliance recommendations"""
        recommendations = []

        # Count status distribution
        status_counts = {'compliant': 0, 'partially_compliant': 0, 'not_implemented': 0}
        for result in control_results.values():
            status_counts[result['status']] += 1

        total_controls = len(control_results)

        # High-level recommendations
        if status_counts['not_implemented'] > total_controls * 0.5:
            recommendations.append(
                "High Priority: More than 50% of controls are not implemented. "
                "Consider establishing a comprehensive security program."
            )

        if status_counts['partially_compliant'] > total_controls * 0.3:
            recommendations.append(
                "Medium Priority: Many controls are partially compliant. "
                "Focus on completing implementation of existing security measures."
            )

        # Technology-specific recommendations
        if 'django' in technology_stack:
            recommendations.append(
                "Django-specific: Leverage Django's built-in security features including "
                "CSRF protection, secure session management, and ORM security."
            )

        if 'fastapi' in technology_stack:
            recommendations.append(
                "FastAPI-specific: Implement dependency injection for security controls "
                "and use Pydantic models for input validation."
            )

        if any(cloud in technology_stack for cloud in ['aws', 'azure', 'gcp']):
            recommendations.append(
                "Cloud-specific: Leverage cloud-native security services and implement "
                "proper IAM policies and network security groups."
            )

        return recommendations

    async def get_security_checklist(self,
                                   technology_stack: List[str],
                                   frameworks: Optional[List[ComplianceFramework]] = None) -> Dict[str, List[str]]:
        """
        Generate security checklist for technology stack
        """
        if frameworks is None:
            frameworks = [ComplianceFramework.OWASP_TOP_10, ComplianceFramework.NIST_CSF]

        checklist = {}

        for framework in frameworks:
            if framework not in self.security_standards:
                continue

            standard = self.security_standards[framework]
            framework_checklist = []

            for control in standard.controls.values():
                if self._is_control_applicable(control, technology_stack):
                    # Create checklist items from verification criteria
                    for criterion in control.verification_criteria:
                        checklist_item = f"[ ] {criterion} ({control.id})"
                        framework_checklist.append(checklist_item)

            checklist[framework.value] = framework_checklist

        return checklist

    async def _standards_update_loop(self):
        """Background loop to update security standards"""
        while True:
            try:
                # Check for updates to security standards
                await self._check_standards_updates()

                # Sleep for configured interval
                sleep_days = self.config['standards']['update_frequency_days']
                await asyncio.sleep(sleep_days * 24 * 3600)

            except Exception as e:
                logger.error(f"Standards update loop error: {e}")
                await asyncio.sleep(24 * 3600)  # Retry after 24 hours

    async def _check_standards_updates(self):
        """Check for updates to security standards"""
        # This would implement actual checking for standard updates
        # For now, just log that we checked
        logger.info("Checked for security standards updates")

    async def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Get compliance dashboard data"""
        dashboard_data = {
            'frameworks_available': len(self.security_standards),
            'total_controls': sum(len(std.controls) for std in self.security_standards.values()),
            'recent_assessments': len(self.assessment_cache),
            'frameworks': {},
            'last_updated': datetime.now().isoformat()
        }

        for framework, standard in self.security_standards.items():
            dashboard_data['frameworks'][framework.value] = {
                'version': standard.version,
                'publication_date': standard.publication_date.isoformat(),
                'control_count': len(standard.controls),
                'domains': list(set(control.domain.value for control in standard.controls.values()))
            }

        return dashboard_data