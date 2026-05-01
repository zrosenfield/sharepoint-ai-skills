Meeting Transcript — Security Policy Review
Date: March 28, 2025
Attendees: Dana Torres, Robin Martinez, Sam Kim

Dana Torres: Alright, let's go through where we are on certifications. As of this month we hold SOC 2 Type II, ISO 27001, and we got our FedRAMP Moderate authorization in January. That was a big lift.

Robin Martinez: The FedRAMP one took what, eight months?

Dana Torres: About ten months end to end. Started the assessment in March last year. The 3PAO engagement alone was four months. But we're authorized now and that opens up the whole federal vertical.

Sam Kim: What about HIPAA?

Dana Torres: We're HIPAA compliant but there's no formal HIPAA certification body the way SOC 2 has one. We have a third-party audit confirming our BAA framework and technical controls meet HIPAA requirements. Last done September 2024.

Robin Martinez: Penetration testing cadence?

Dana Torres: External pen tests annually through CrowdStrike. Last one November 2024, clean report, no critical findings. We do internal vulnerability scanning weekly through Qualys. High or critical gets a 72-hour remediation SLA. Medium gets 30 days.

Robin Martinez: Why CrowdStrike specifically?

Dana Torres: We actually used Rapid7 before 2023. They were fine for standard pen testing but when we started the FedRAMP prep we needed a firm with FedRAMP assessment experience. CrowdStrike had done assessments for three companies in our space and knew the control mapping. We ran both in parallel for one cycle — Rapid7 found 12 issues, CrowdStrike found 19, including three that were specifically relevant to FedRAMP moderate controls. That settled it.

Sam Kim: Network segmentation — can we guarantee tenant isolation?

Dana Torres: Yes. Every customer environment runs in an isolated VPC. No shared compute, no shared storage at the data layer. Control plane is shared but all customer data paths are fully isolated. Architecture since the 2023 redesign.

Robin Martinez: What drove the redesign?

Dana Torres: The Meridian incident. October 2022. A configuration error in the shared environment allowed one tenant's background job to read another tenant's queue. No data was actually exposed — the job errored before processing — but the fact that it was possible was unacceptable. We spent Q1 2023 rebuilding with full VPC isolation. Cost us about $2M in infrastructure and delayed two product launches, but it was the right call. Haven't had a single isolation concern since.

Sam Kim: Data retention after contract termination?

Dana Torres: 30 days. Customer data retained for 30 days post-termination, they can request an export during that window. After 30 days, permanently deleted. Backups purged within 90 days. That's in the MSA template, section 8.3.

Sam Kim: Was it always 30 days?

Dana Torres: It was 90 days originally. We shortened it in 2024 after legal reviewed the liability exposure. Holding customer data longer than necessary after termination creates risk — if there's a breach during that window, we're still responsible. 30 days is enough for any reasonable export request and reduces our exposure window by two thirds.

Robin Martinez: I think that covers the main questions. Thanks Dana.
