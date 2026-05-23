# Paper List: FPGA-Based BCD Adder System

## 1. Design of a High Speed BCD Adder
**Authors:** A. N. Jayanthi, C. S. Ravichandran  
**Objective:** High-speed BCD adder design with reduced delay through increased parallelism.  
**Methodology:** Optimized carry network, conventional vs proposed comparison.  
**Key Findings:** Delay significantly reduced compared with conventional design.  
**Limitations:** Focus mainly on speed, less FPGA resource analysis.  
**Relevance:** Very high.
**Link:** https://www.researchgate.net/publication/291876203_Design_of_a_high_speed_BCD_adder

## 2. Hardware Modeling of Binary Coded Decimal Adder in FPGA
**Authors:** Muhammad Ibn Ibrahimy, Md. Rezwanul Ahsan, Iksannurazmi B. Soeroso  
**Objective:** FPGA implementation of BCD adder.  
**Methodology:** Verilog HDL, Altera Quartus II, CLA vs Ripple Carry comparison.  
**Key Findings:** CLA faster and more efficient.  
**Limitations:** Older FPGA platform.  
**Relevance:** Very high.
**Link:** https://www.researchgate.net/publication/260449465_Hardware_Modeling_of_Binary_Coded_Decimal_Adder_in_FPGA

## 3. Evaluating Sensor Data Quality in Internet of Things Smart Agriculture Applications
**Authors:** Kaneez Fizza et al.  
**Objective:** IoT sensor data quality evaluation.  
**Methodology:** Sensor stream quality framework.  
**Key Findings:** Useful IoT quality model.  
**Limitations:** Not related to BCD adder.  
**Relevance:** None.
**Link:** https://arxiv.org/abs/2105.02819


## 4. Decimal Addition on FPGA Based on a Mixed BCD/Excess-6 Representation
**Authors:** Horácio Neto, Mário Véstias  
**Objective:** Improve decimal addition on FPGA.  
**Methodology:** Mixed BCD/Excess-6 representation, LUT optimization.  
**Key Findings:** Better FPGA efficiency and speed.  
**Limitations:** Higher implementation complexity.  
**Relevance:** Very high.
**Link:** https://www.sciencedirect.com/science/article/abs/pii/S0141933116303908

## 5. A Fast FPGA-Based BCD Adder
**Authors:** Mubin Ul Haque, Zarrin Tasnim Sworna, Hafiz Md. Hasan Babu, Ashis Kumer Biswas  
**Source:** Circuits, Systems, and Signal Processing, Springer, 2018  
**Objective:** Design a high-speed BCD adder optimized for FPGA using LUT-based implementation.  
**Methodology:** LUT-based decimal adder architecture for FPGA; performance comparison with prior BCD adder designs.  
**Key Findings:** Proposed design achieves improved speed for FPGA-based decimal processing.  
**Limitations:** Focus on adder speed; less emphasis on broader system integration.  
**Relevance:** Very high — directly related to FPGA-based BCD adder optimization.  
**Link:** https://link.springer.com/article/10.1007/s00034-018-0770-3

## 6. Reduced Delay BCD Adder
**Authors:** Alp Arslan Bayrakci, Ahmet Akkas  
**Source:** IEEE International Conference on Application-specific Systems, Architectures and Processors (ASAP), 2007  
**Objective:** Reduce delay in BCD addition through increased parallelism.  
**Methodology:** Parallel BCD adder structure; delay-oriented optimization compared with conventional BCD adders.  
**Key Findings:** Demonstrates significant delay reduction via parallel carry handling.  
**Limitations:** Classic ASIC-oriented design; limited modern FPGA LUT analysis.  
**Relevance:** Very high — useful for comparing conventional and optimized BCD adders.  
**Link:** https://www.computer.org/csdl/proceedings-article/asap/2007/04429991/12OmNzd7bzY

## 7. Decimal Adders/Subtractors in FPGA: Efficient 6-input LUT Implementations
**Authors:** M. Vazquez, G. Sutter, G. Bioul, J. P. Deschamps  
**Source:** IEEE International Conference on Reconfigurable Computing and FPGAs (ReConFig), 2009  
**Objective:** Efficient FPGA implementation of decimal adders and subtractors using 6-input LUT architectures.  
**Methodology:** LUT-mapped decimal arithmetic units optimized for Xilinx 6-input LUT FPGAs.  
**Key Findings:** Achieves efficient area and delay for decimal add/subtract on FPGA.  
**Limitations:** Platform-specific to 6-input LUT FPGA families.  
**Relevance:** Very high — useful for FPGA resource optimization in decimal arithmetic.  
**Link:** https://www.computer.org/csdl/proceedings-article/reconfig/2009/3917a042/12OmNqJq4Aq

## 8. High-Speed Multioperand Decimal Adders
**Authors:** Robert D. Kenney, Michael J. Schulte  
**Source:** IEEE Transactions on Computers, 2005  
**Objective:** Design high-speed multioperand decimal adders for decimal accumulation workloads.  
**Methodology:** Multioperand decimal addition architecture; performance analysis for high-speed decimal processing.  
**Key Findings:** Provides strong reference designs for fast multioperand decimal addition.  
**Limitations:** General decimal arithmetic focus; not specific to IoT sensor pipelines.  
**Relevance:** High — useful if the project accumulates multiple sensor values or aggregates decimal readings.  
**Link:** https://dl.acm.org/doi/abs/10.1109/TC.2005.129

## 9. Data Quality Assessment and Analysis for Pest Identification in Smart Agriculture
**Authors:** Jiachen Yang, Guipeng Lan, Yang Li, Yicheng Gong, Zhuo Zhang, Sezai Ercisli  
**Source:** Computers and Electrical Engineering, Elsevier, 2022  
**Objective:** Assess and analyze data quality for pest identification in smart agriculture systems.  
**Methodology:** Data quality assessment framework applied to agricultural pest identification datasets.  
**Key Findings:** Poor data quality reduces model reliability and decision accuracy in smart agriculture.  
**Limitations:** Domain-specific to pest identification; not a general IoT hardware paper.  
**Relevance:** Medium — supports arguments for data quality validation in agricultural AI systems.  
**Link:** https://www.sciencedirect.com/science/article/abs/pii/S0045790622005444

## 10. IoT Data Quality Assessment Framework Using Adaptive Weighted Estimation Fusion
**Authors:** J. Byabazaire et al.  
**Source:** Sensors, MDPI, 2023  
**Objective:** Provide a general IoT data quality assessment framework with adaptive fusion.  
**Methodology:** Adaptive weighted estimation fusion for sensor validation, reliability scoring, and data fusion.  
**Key Findings:** Framework improves reliability assessment and fusion quality in IoT deployments.  
**Limitations:** Framework-level contribution; less focus on FPGA decimal arithmetic.  
**Relevance:** Medium — useful for sensor validation and data fusion in AIoT systems.  
**Link:** https://www.mdpi.com/1424-8220/23/13/5993

## 11. Artificial Intelligence of Things (AIoT) for Smart Agriculture: A Review of Architectures, Technologies and Solutions
**Authors:** Dalhatu Muhammed, Ehsan Ahvar, Shohreh Ahvar, Maria Trocan, Marie-José Montpetit, Reza Ehsani  
**Source:** Journal of Network and Computer Applications, Elsevier, 2024  
**Objective:** Review AIoT architectures, technologies, and solutions for smart agriculture.  
**Methodology:** Systematic review of sensors, machine learning, connectivity, and smart agriculture system designs.  
**Key Findings:** Comprehensive overview of AIoT stack for agricultural monitoring and decision support.  
**Limitations:** Review paper; no specific BCD adder or FPGA implementation details.  
**Relevance:** Medium — useful for framing the overall AIoT architecture of the project.  
**Link:** https://www.sciencedirect.com/science/article/pii/S1084804524000821

## 12. Smart Sustainable Greenhouses Utilizing Microcontroller and IOT in the GCC Countries; Energy Requirements & Economical Analyses Study for a Concept Model in the State of Qatar
**Authors:** Salem Al-Naemi, Awni Al-Otoom  
**Source:** Results in Engineering, Elsevier, 2023  
**Objective:** Design and analyze a smart sustainable greenhouse concept using microcontrollers and IoT.  
**Methodology:** Microcontroller/IoT-based greenhouse model; temperature, humidity, irrigation control; energy and cost analysis for Qatar.  
**Key Findings:** Demonstrates feasibility of IoT greenhouse control with energy and economic considerations.  
**Limitations:** Concept model study; limited AI/RAG decision-support integration.  
**Relevance:** Medium — useful for application domain and greenhouse system design.  
**Link:** https://www.sciencedirect.com/science/article/pii/S2590123023000166

## 13. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
**Authors:** Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela  
**Source:** NeurIPS, 2020  
**Objective:** Combine retrieval with generation for knowledge-intensive NLP tasks.  
**Methodology:** Retrieval-augmented generation (RAG) pipeline: retrieve relevant documents, then condition a generator on retrieved context.  
**Key Findings:** RAG improves factual accuracy and performance on knowledge-intensive tasks.  
**Limitations:** NLP-focused; requires adaptation for agricultural sensor/decision domains.  
**Relevance:** Medium — foundational reference for Agentic RAG decision-support in the system.  
**Link:** https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

## 14. Impact of Radix-10 Redundant Digit Set [-6, 9] on Basic Decimal Arithmetic Operations
**Authors:** Ghassem Jaberipur, Farzad Ghazanfari  
**Source:** IEEE Transactions on Very Large Scale Integration (VLSI) Systems, 2022  
**Objective:** Analyze how radix-10 redundant digit set [-6, 9] affects basic decimal arithmetic operations.  
**Methodology:** Redundant decimal representation analysis; evaluation of addition and related decimal operations.  
**Key Findings:** Alternative decimal representations can improve efficiency of basic decimal arithmetic.  
**Limitations:** Theoretical/VLSI-oriented; not FPGA greenhouse application specific.  
**Relevance:** High — advanced decimal arithmetic reference complementary to BCD adder designs.  
**Link:** https://doi.org/10.1109/TVLSI.2021.3120065

## 15. AI-powered Sensor Fault Detection for Cost-effective Smart Greenhouses
**Authors:** Seyed Mohammadhossein Shekarian, Mahdi Aminian, Amir Mohammad Fallah, Vaha Akbary Moghaddam  
**Source:** Computers and Electronics in Agriculture, Elsevier, Volume 224, 2024, Article 109198  
**Objective:** Detect sensor faults in smart greenhouses using AI for cost-effective reliable monitoring.  
**Methodology:** AI-based fault detection on greenhouse sensor data; practical deployment for smart agriculture.  
**Key Findings:** AI fault detection improves reliability and cost-effectiveness of greenhouse sensor systems.  
**Limitations:** Focus on fault detection, not decimal arithmetic hardware.  
**Relevance:** Medium — supports sensor reliability and quality assurance in the application domain.  
**Link:** https://doi.org/10.1016/j.compag.2024.109198

