# MambaNA: A state space model with Neighborhood Attention for Medical Super-Resolution

## Anonymous CVPR submission

## Paper ID *****

## Abstract

In recent years, due to Mamba’s ability to balance global 001

receptive fields and computational efficiency, Mamba-based 002

methods have demonstrated significant potential in various 003

tasks, including medical image super-resolution. However, 004

the inherent causal modeling of Mamba restricts its local 005

feature extraction, this poses a challenge for medical im- 006

age super-resolution which often involves intricate local 007

details in structures like cells and tissue boundaries. In 008

this work, we propose MambaNA, a novel medical image 009

super-resolution method that integrates neighborhood at- 010

tention mechanism into Mamba model. Specifically, Mam- 011

baNA computes pixel-wise attention weights for neighbor- 012

ing elements to introduce non-causality, while extracting lo- 013

cal features that maintain translational equivariance. Fur- 014

thermore, it performs a multi frequency channel fusion di- 015

rectly following SSM’s sequence modeling, which signifi- 016

cantly boosts model performance and training stability. Ex- 017

tensive experiments demonstrated the superior performance 018

of MambaNA in medical image super-resolution tasks. Key- 019

words: Medical imaging · Super-Resolution · Mamba 020

## 1. Introduction 021

Modern medical diagnosis heavily relies on the visual infor- 022

mation provided by medical imaging. However, obtaining 023

high-quality images often involves costly advanced equip- 024

ment and extended patient exposure. Deep learning ad- 025

vances have made super-resolution (SR) an economically 026

efficient solution for image enhancement, capable of intel- 027

ligently reconstructing fine structures from low-resolution 028

inputs. In the medical domain, SR specifically focuses 029

on generating high-resolution outputs from low-resolution 030

scans by inferring and synthesizing intricate details typi- 031

cally lost during acquisition. 032

Early super-resolution research, relying on simple inter- 033

polation [10, 12, 25] and optimization [48] methods, was 034

age details. Subsequently, Convolutional Neural Networks 036 (CNNs) [7, 8, 27, 29, 63, 64] and Generative Adversarial 037 Networks (GANs) [27, 52, 53] gained widespread appli- 038 cation due to their ability to learn nonlinear mapping re- 039 lationships and representational features. However, these 040 methods frequently struggled with capturing long-range de- 041 pendencies and global receptive fields, which limited their 042 ability to restore high-frequency details and maintain struc- 043 tural coherence, leading to sub-optimal reconstruction qual- 044 ity, especially in complex medical imagery. 045 To mitigate these limitations, the Transformer architec- 046 ture [50], with its powerful self-attention mechanism for 047 global dependency modeling, has been successfully adapted 048 to computer vision, notably through the Vision Transformer 049 (ViT) [2, 6, 9, 30, 54], demonstrating efficacy in captur- 050 ing long-range spatial relationships. Despite this strength, 051 Transformer-based methods often incur considerable com- 052 putational and memory costs, largely due to the quadratic 053 scaling of their global self-attention. State Space Mod- 054 els (SSMs) [16, 17, 47] have emerged as a class of deep 055 sequence models designed to efficiently process long se- 056 quences by transforming inputs into a hidden state space. 057 Among these, the Mamba architecture [15] stands out as a 058 notable advancement, effectively balancing global receptive 059 fields with computational efficiency. However, Mamba’s in- 060 herent causal modeling limits its ability to fully exploit vi- 061 tal local features [19], a constraint especially pronounced in 062 medical images where fine, localized details are crucial for 063 precise analysis. 064 To address these crucial limitations, we propose Mam- 065 baNA, a novel medical image super-resolution method. It 066 integrates Neighborhood Attention (NA) [21] into a Mamba 067 architecture to introduce non-causal modeling and mitigate 068 Mamba’s inherent causal limitations, while concurrently 069 enhancing its local feature extraction. Furthermore, Mam- 070 baNA incorporates a lightweight multi-spectral channel at- 071 tention (MSCA) [40] based on the Discrete Cosine Trans- 072 form (DCT), which extends traditional channel attention by 073 fusing multi-frequency components. This allows the model 074 to capture intricate frequency-domain patterns and cross- 075

straightforward but often failed to precisely restore im- 035

channel dependencies, and experimental results show that 076

this incorporation significantly boosts MambaNA’s perfor- 077

mance and training stability. The main contributions of this 078

paper are summarized as follows: 079

## 1. We build a Mamba-based network for medical image 080

super-resolution called MambaNA. It combines the ad- 081

vantages of Mamba’s global receptive fields and spatial 082

attention mechanism’s non-causal modeling, achieving 083

and TransMRSR [23] explored combining CNNs’ local 127 strengths with Transformer-based global modeling for 3D 128 MRI. Others such as [67] and [28] introduced frequency- 129 based strategies for MRI, while [1] leveraged Vision Trans- 130 formers in self-supervised microscopy SR. However, most 131 of these methods require substantial GPU memory and 132 training cost. Despite this, their ability to model global con- 133 text makes them valuable for SR tasks that demand high 134 structural fidelity. 135

greater efficiency and accuracy in processing complex 084

medical images. 085

### 2.2. State Space Models 136

## 2. We propose an SSM-Layer which incorporates a channel 086

attention mechanism that directly follows the SSM mod- 087

ule. It captures intricate patterns and suppresses noise 088

by adaptively weighting different frequency components 089

within channels, thereby boosting MambaNA’s overall 090

performance and enhancing its training stability. 091

## 3. We conducted extensive experiments on various tasks 092

and performed ablation studies to verify each key com- 093

ponent’s contribution. The results show that MambaNA 094

outperforms existing state-of-the-art methods across sev- 095

eral key metrics, demonstrating its effectiveness and ro- 096

bustness across different scenarios. 097

## 2. Related Works 098

### 2.1. Medical Image Super-Resolution 099

While traditional methods often lack detail fidelity and ar- 100

tifact suppression, deep learning has profoundly advanced 101

medical image SR, yielding numerous CNN-based and 102

GAN-based algorithms. 103

CNNs are widely adopted for medical image SR due to 104

their powerful feature extraction and end-to-end learning. 105

Early works like SRCNN [8] and VDSR [26] were extended 106

to medical contexts such as CT and MRI [38, 49]. Sub- 107

sequent advancements incorporated sophisticated architec- 108

tural designs. These include various forms of residual learn- 109

ing [37, 39, 41, 45, 65] and dense connections [3, 5, 42]. 110

Such innovations facilitate deeper network training and en- 111

hance feature reuse, significantly improving performance 112

SSMs have recently attracted increasing interest for se- 137 quence modeling due to their potential to overcome the 138 efficiency limitations of RNNs and Transformers on long 139 sequences. The Mamba architecture [15] introduces a Se- 140 lective State Space Model (Selective SSM) that adaptively 141 modulates state space parameters based on input content, 142 enabling efficient long-range dependency modeling. It has 143 demonstrated competitive or even superior performance to 144 Transformers in language modeling tasks [57]. 145 Despite Mamba’s strong sequence modeling perfor- 146 mance, its direct application to vision tasks faces challenges 147 due to the 2D non-causal nature of image pixels and its 148 inherent causal modeling. This causality limits full pixel 149 utilization and can lead to decayed long-range dependen- 150 cies. Researchers have addressed this by developing various 151 scanning strategies to adapt 2D image data for Mamba’s 1D 152 causal processing. For instance, VMamba [33] pioneered 153 cross-scan strategies for general vision tasks. ViM [68] 154 employs bidirectional scanning with position embeddings, 155 while PlainMamba [58] utilizes continuous 2D scanning 156 and direction-aware updates to capture spatial relationships. 157 Furthermore, LocalMamba [24] introduces dynamic, layer- 158 specific optimal scan choices within distinct image win- 159 dows. Building upon these advancements, Mamba-based 160 models have rapidly become prominent in various computer 161 vision domains [18, 19, 43, 55, 66]. These innovations 162 enable SSMs to effectively process 2D visual data, cap- 163 ture global context, and achieve competitive performance 164 against Transformers [57, 62]. 165

across diverse medical image modalities for clinical ap- 113

plications [20, 44]. GANs excel at generating perceptu- 114

### 2.3. Attention Mechanisms 166

ally richer HR medical images and can mitigate the over- 115

smoothing seen with CNNs. For instance, GANs have been 116

utilized for denoising and SR of low-dose CT [56, 60], or 117

combined with CycleGAN for improved CT reconstruction 118

[61]. Additionally, architectural integrations like DCSRN 119

within the GAN framework [4], and specific adversarial 120

networks for CMRI [35] or compressed sensing MRI [59], 121

demonstrate enhanced performance. 122

Transformer architectures have recently gained atten- 123

tion in SR for their ability to model long-range depen- 124

dencies and global semantic features better than tradi- 125

tional CNNs. For instance, models like SuperFormer [11] 126

In deep learning models, channel attention mechanisms en- 167 able dynamic focus on critical input features. They model 168 inter-channel relationships, learning adaptive weights to ef- 169 ficiently allocate computational resources and enhance fea- 170 ture representation. SENet [22] pioneered this field with 171 its Squeeze-and-Excitation (SE) module, which aggregates 172 global spatial information via global average pooling and 173 then learns channel dependencies. To mitigate information 174 loss from traditional global average pooling, FcaNet [40] 175 introduced Multi-Spectral Channel Attention using Discrete 176 Cosine Transform for frequency-domain analysis. Further- 177

more, ECA-Net [51] employs a 1D convolution for efficient 178

local cross-channel interaction without dimensionality re- 179

duction. 180

Spatial attention mechanisms, on the other hand, high- 181

The discretized form allows SSMs to be integrated into 222 deep learning architectures efficiently, and Eq. (3) can be 223 accelerated via parallel computation, leveraging a global 224 convolution operation: 225

light the importance of different spatial locations within 182

a feature map. The emergence of ViT [9] marked a 183

¯K = (C ¯B, C ¯A ¯B, . . . , C ¯AL−1¯B),

paradigm shift in computer vision, demonstrating that 184

y = x ⊛¯K, (4) 226

pure self-attention architectures could achieve competi- 185

tive performance with CNNs by modeling long-range de- 186

pendencies. Swin Transformer [34] introduced a Shifted 187

Window (Swin) Attention, which computes self-attention 188

within non-overlapping local windows and allows for cross- 189

window connections through a shifted window partition- 190

ing approach. Beyond these general advancements, the lat- 191

where ⊛stands for the convolution operation, L is input 227 sequence’s length, and¯K ∈RLrepresents the convolution 228 kernel. By utilizing convolution, this method enables the 229 simultaneous computation of outputs across the sequence, 230 which significantly improves computational efficiency and 231 scalability. 232

est efforts, highlight a strong emphasis on synergistic and 192

dual attention mechanisms to enhance feature representa- 193

#### 3.1.2. Mamba: Selective State Space Models 233

tion across various vision tasks, as exemplified by works 194

such as SCSA [46], DACN [36], CATA-TCN [32], and 195

TSCA-Net [13], demonstrating powerful potential in areas 196

like super-resolution and medical image processing. 197

## 3. Methodology 198

### 3.1. Preliminaries 199

#### 3.1.1. State Space Models 200

SSMs are a class of models inspired by control systems 201

theory for sequence modeling. They have recently gained 202

attention in deep learning for their ability to handle long- 203

range dependencies efficiently. The core idea of SSMs is to 204

model the relationship between an input sequence x ∈R 205

and an output sequence y ∈R through a hidden state 206

Mamba [15] is a novel variant of SSMs that extends the 234 S4 framework [16] by incorporating a data-dependent pa- 235 rameterization. This allows Mamba to leverage the lin- 236 ear computational complexity with respect to the input se- 237 quence length for highly efficient, content-aware processing 238 of long sequences. Mamba surpasses Transformers in per- 239 formance on large-scale real data, showcasing its effective- 240 ness across various sizes and demonstrating linear scalabil- 241 ity in sequence length. 242 The key innovation of Mamba lies in its selective mecha- 243 nism, which adjusts the parameters B, C, ∆based on the in- 244 put sequence. This allows the model to dynamically capture 245 the characteristics of long-sequence signals using a sim- 246 ple architecture. The selective mechanism uses the input 247 x ∈RB×L×Dto generate input-dependent parameters: 248

h ∈RN. Formally, a continuous-time SSM can be defined 207

by a set of linear ordinary differential equations (ODEs): 208

B ∈RB×L×N←sB(x),

h′(t) = Ah(t) + Bx(t),

(5) 249

C ∈RB×L×N←sC(x),

y(t) = Ch(t) + Dx(t), (1) 209

∆∈RB×L×D←s∆(x),

where N is the state size, A ∈RN×N, B ∈RN×1, and C ∈ 210

R1×Nare the system matrices governing the state dynamics 211

and output mapping, and D ∈R is the skip connection 212

weight. 213

To make SSMs applicable in deep learning scenarios, 214

the continuous-time model is discretized. Using the zero- 215

order hold (ZOH) assumption, the continuous-time param- 216

eters A, B are converted to discrete parameters¯A,¯B over a 217

specified sampling interval ∆∈R > 0: 218

¯A = e∆A, ¯B = (∆A)−1(e∆A−I) · ∆B. (2) 219

This leads to a discrete-time model formulation: 220

ht = ¯Aht−1 + ¯Bxt,

where s(·) is typically implemented using a linear projec- 250 tion layer. Mamba shares the same recursive form of the 251 hidden state update Eq. (3), which enables the model to 252 memorize ultra-long sequences so that more pixels can be 253 activated to aid restoration. 254 For exceptional efficiency, Mamba introduces a special- 255 ized parallel algorithm for its recurrent mode, this algorithm 256 is meticulously designed to optimize memory access and 257 minimize redundant computations on modern accelerators, 258 thereby ensuring efficient inference. Complementing this, 259 Mamba adopts a simplified end-to-end neural network ar- 260 chitecture that entirely eschews attention modules and even 261 traditional MLP blocks. This architectural parsimony, cen- 262 tered around the selective SSM layer, significantly reduces 263 parameter count and computational overhead, leading to 264 faster training and inference times. 265

yt = Cht + Dxt. (3) 221

Figure 1. Overall Architecture

### 3.2. Overall Architecture 266

As depicted in Figure 1, MambaNA is composed of three 267

modules: shallow feature extraction, deep feature extrac- 268

tion and HQ image reconstruction modules, which aligns 269

with the prevalent architectural paradigms of image restora- 270

tion Transformer networks [30]. Given a LQ input image 271

ILQ ∈RH×W ×Cin, it first undergoes shallow feature ex- 272

traction, typically implemented as a single 3 × 3 convolu- 273

Figure 2. MambaNA’s Attention Block

tional layer. This process transforms the input into initial 274

features F0 ∈RH×W ×C, which retain the original spatial 275

dimensions while expanding the channel depth. The subse- 276

### 3.3. Attention Block 297

quent deep feature extraction stage, where the core process- 277

ing and our novel enhancements are applied, is responsible 278

for extracting complex hierarchical features. 279

Specifically, this stage comprises a stack of N1 resid- 280

ual MambaNA groups (MNAGs). Within each MNAG, 281

N2 cascaded MambaNA Blocks (MNABs) are utilized for 282

core feature transformation. Each MNAB, in turn, is com- 283

posed of an Attention Block and a SSM-layer, collectively 284

performing the detailed feature extraction and refinement. 285

Upon completion of this deep feature extraction stage, the 286

initial features F0 are progressively transformed into refined 287

MambaNA incorporates the Neighborhood Attention (NA) 298 mechanism [21] as a pivotal attention extraction module 299 to incorporate non-causal modeling ability and at the same 300 time, enhance the perception of intricate image details. 301 NA attention employs a sliding window paradigm to per- 302 form self-attention operations. Unlike global self-attention 303 or conventional window-based attention, NA strictly con- 304 fines each query pixel’s attention computation to its prede- 305 fined fixed-size local neighborhood. Specifically, given an 306 input X ∈RN×d, it will continuously calculate the adjacent 307 attention of the i-th input: 308

deep features FN1 ∈RH×W ×C. Finally, the HQ image re- 288

construction module leverages these refined deep features 289

Ak i= QiKT N(i)+ Bi,

to progressively reconstruct the desired HQ output image. 290

For the task of medical image super-resolution, Mam- 291

NAk(i) = softmax(Ak i √

d)VN(i). (7) 309

baNA is optimized using a hybrid loss function combining 292

ℓ1 loss and perceptual loss. The final loss is defined as: 293

L = 0.7 · LL1 + 0.3 · Lperceptual,

(6) 294

Lℓ1 = ||IHQ −IGT ||1,

Lperceptual = ||ϕ(IHQ) −ϕ(IGT )||2 2

where ϕ(·) denotes feature extraction from pre-trained 295

VGG-19’s 5th conv layer. 296

Here, k is the neighborhood size, Bi ∈R1×kis the relative 310 positional biases, and Qi ∈R1×d, KN(i) ∈Rk×d, VN(i) ∈ 311 Rk×dare respectively the i-th input’s query, key, and value 312 matrix where N(i) represents the i-th element’s neighbor- 313 hood. This localized design of NA inherently incorporates 314 local inductive bias and ensures translational equivariance 315 to patterns appearing at different positions within the im- 316 age. 317

### 3.4. SSM-Layer 352

Figure 3. MambaNA’s SSM-Layer

In MambaNA, the SSM-Layer is designed to efficiently cap- 353 ture long-range dependencies with the state space equa- 354 tion. Conventional selective SSMs often process 2D im- 355 age data by linearizing it into 1D sequences via fixed, 356 data-independent scanning sequences. This rigid method- 357 ology often hinders a query pixel from effectively utilizing 358 spatially distant yet semantically similar already-processed 359 pixels, thereby failing to capture comprehensive non-causal 360 global context. To address this limitation and circum- 361 vent the inherent inefficiencies and computational redun- 362 dancy associated with employing multiple fixed scanning 363 sequences, SSM-Layer employs a dynamic pixel scanning 364 strategy predicated on semantic categorization. 365 Given feature map X ∈RC×H×W, we first compute a 366 semantic relevance score for each pixel: 367

s(i) = MLP(GAP(Xi)), (8) 368

Compared to window-based attention mechanisms like 318

Swin, NA is better suited for capturing the rich and fine lo- 319

where i indexes spatial locations and GAP extracts local 369 statistics from a k × k neighborhood. Pixels are then softly 370 grouped by quantizing s(i) into G semantic bins: 371

cal details prevalent in medical images, such as subtle vas- 320

cular textures or lesion boundaries. This is primarily be- 321

g(i) = ⌊G · σ(s(i))⌋. (9) 372

cause Swin’s fixed window partitioning can lead to high- 322

frequency information loss or processing discontinuities at 323

window boundaries, whereas NA’s overlapping sliding win- 324

For each group, pixels preserve their 2D raster order, while 373 the final 1D scan sequence π is formed by concatenating 374 groups from low to high semantic relevance: 375

dows provide a smoother, more continuous context aggre- 325

gation, and its inherent translational equivariance is crucial 326

π = concat(πg=0, πg=1, ..., πg=G−1). (10) 376

for medical image super-resolution. Furthermore, NA also 327

efficiently expands the receptive field through multi-layer 328

stacking without incurring the high computational cost of 329

global attention, making it particularly effective for high- 330

resolution medical image processing without complex shift- 331

ing operations as seen in Swin. 332

Theoretically, the integration of NA attention with 333

Mamba models can yield a powerful synergy. Mamba mod- 334

els excel at efficiently capturing long-range dependencies 335

and global structural information through their selective 336

scan mechanisms, thereby ensuring overall image coher- 337

ence. However, being fundamentally 1D sequence-based, 338

their ability to model dense, non-linear local spatial re- 339

lationships in 2D images might be less specialized than 340

dedicated local operations. NA attention precisely com- 341

plements this, focusing on providing fine-grained local in- 342

ductive bias and efficient pixel-level spatial interactions. 343

Consequently, this integration allows MambaNA to possess 344

both remarkable global consistency and precise local de- 345

tail rendering capabilities. This “global-local” synergistic 346

This adaptive ordering reduces semantic distance in the 377 SSM sequence while maintaining O(HW) complexity. 378 After assigning a definitive semantic category to each 379 pixel, these pixels are then reordered according to their re- 380 spective categories to construct the final one-dimensional 381 scanning sequence. This methodology ensures that seman- 382 tically similar pixels are prioritized during the state update 383 process within the SSM, thereby mitigating the weakening 384 effect of remote pixel interactions caused by long-range de- 385 cay. 386 Given that medical images encompass rich details, tex- 387 tures, and overall structures, which correspond to high, 388 mid, and low-frequency information respectively, we strate- 389 gically integrated the Multi-Spectral Channel Attention 390 (MSCA) module subsequent to the SSM-Layer. Specifi- 391 cally, MSCA precisely extracts multiple frequency compo- 392 nents from the spatial information within each channel by 393 applying a fixed bank of pre-computed 2D DCT basis func- 394 tions as filters. These extracted frequency responses then 395 form the multi-spectral content, based on which MSCA 396 learns scaling factors w for channels: 397

processing paradigm is especially vital for medical image 347

super-resolution, as it necessitates both the restoration of 348

H−1 X

W −1 X

Freqi=

large-scale anatomical integrity and the meticulous recon- 349

(11) 398

w=0 Xi,h,w· DCTi,h,w,

h=0

struction of minute pathological details to ensure diagnostic 350

accuracy. 351

Freq = cat( Freq1 Freq2 · · · FreqC),

w = σ(MLP(Freq)). (12) 399

Here, X ∈RC×H×Wis the input feature map, and DCT ∈ 400

RC×H×Wis the 2D DCT basis filter. 401

The integration of the MSCA module significantly 402

the optimizer with β1 = 0.9, β2 = 0.99. The initial learn- 446 ing rate and batch size are respectively set at 2 × 10−4and 447 2. Additionally, we crop the original images into 64 × 64 448 patches during training. We set up six Mamba blocks and 449 each block’s channel count is 192. 450

boosts MambaNA’s performance and its training stabil- 403

ity. This stability enhancement fundamentally arises from 404

### 4.2. Comparison on Image Super-Resolution 451

MSCA’s capacity for frequency-aware feature conditioning 405

and adaptive channel regulation, which is particularly per- 406

tinent for SSMs. While SSM adeptly aggregates global 407

spatio-sequential information, its inherent one-dimensional 408

processing of two-dimensional image data can render it 409

acutely sensitive to the conditioning, noise, and distribu- 410

tional properties of individual feature channels, potentially 411

propagating instabilities through recurrent state updates. 412

By instilling robust channel-wise feature representations, 413

MSCA effectively acts as a frequency-domain filter and pro- 414

vide a powerful adaptive normalization and magnitude con- 415

trol for each channel, enabling optimizers to converge more 416

reliably and efficiently. 417

## 4. Experiments 418

### 4.1. Experimental Settings 419

#### 4.1.1. Datasets and Metrics 420

Our experiments utilized two publicly available medical 421

image super-resolution datasets: IXI1dataset and a ded- 422

icated Brain Tumor MRI dataset2. The IXI dataset in- 423

cludes 3D multimodal MRI scans (T1, T2, PD modali- 424

ties). We focused on the T1-weighted subset (IXI-T1) for 425

SR training/testing, given its superior brain soft tissue con- 426

trast. Each original IXI-T1 scan contains 96 slices (240 × 427

## 240 pixels); we uniformly selected 8 key slices per scan to 428

avoid redundant low-variation samples. The IXI-T1 dataset 429

was split as follows: 600 slices for training, 64 slices for 430

validation, and 84 slices from remaining qualified T1 scans 431

for testing. All slices retain the 240 × 240 pixel resolution. 432

To quantitatively evaluate the quality of the super- 433

resolved images, we selected the widely recognized met- 434

rics: Peak Signal-to-Noise Ratio (PSNR) and the Structural 435

Similarity Index Measure (SSIM). PSNR measures pixel- 436

wise fidelity by comparing reconstructed images to ground 437

truth, while SSIM assesses perceptual similarity based on 438

luminance, contrast, and structure. 439

#### 4.1.2. Experimental Details 440

Our comprehensive evaluation first focused on validating 452 MambaNA’s performance against existing state-of-the-art 453 (SOTA) medical image super-resolution methods on the 454 challenging IXI dataset. As detailed in Table 1, MambaNA 455 consistently achieves superior PSNR and SSIM scores com- 456 pared to [14], [19], and [30]. These quantitative results 457 underscore MambaNA’s exceptional ability to reconstruct 458 high-fidelity medical images, effectively balancing global 459 context modeling with precise local detail recovery. 460 Beyond numerical metrics, Figure 4 provides a com- 461 prehensive qualitative comparison of the super-resolution 462 results: the first row displays the reconstructed images 463 from various methods, while the second row presents pixel- 464 wise mean squared error (MSE) maps between each super- 465 resolved image and the ground truth, allowing for an intu- 466 itive understanding of reconstruction accuracy. Darker re- 467 gions in the error maps indicate smaller deviations from 468 the ground truth, signifying better reconstruction fidelity. 469 As visually demonstrated, MambaNA produces reconstruc- 470 tions notably closer to the ground truth, with error maps 471 revealing a significant reduction in artifacts and a more ac- 472 curate preservation of finer anatomical structures compared 473 to other methods that often exhibit blurring or false details 474 in challenging areas. This pronounced qualitative superior- 475 ity further reinforces MambaNA’s practical utility in clinical 476 image analysis. 477 To assess MambaNA’s generalization capabilities, we 478 also evaluated its performance on widely recognized nat- 479 ural image super-resolution benchmark datasets, includ- 480 ing BSDS100, Urban100, and Manga109. As presented 481 in Table 3, MambaNA consistently achieves state-of-the- 482 art (SOTA) or near-SOTA performance in terms of PSNR 483 and SSIM across these datasets, demonstrating its compet- 484 itiveness against various established natural image super- 485 resolution algorithms. This indicates that MambaNA’s de- 486 sign, while optimized for medical images, effectively trans- 487 fers its robust super-resolution capabilities to diverse nat- 488 ural image scenarios, highlighting its versatility and broad 489 applicability. 490

Our MambaNA is implemented with the PyTorch toolbox 441

and trained on NVIDIA RTX A6000 GPU. The training 442

### 4.3. Ablation Study 491

low-resolution samples are generated by the frequency do- 443

main method, ensuring a closer alignment with the actual 444

distribution of low-resolution images. We adopt Adam as 445

1https://brain-development.org/ixi-dataset/2https://www.kaggle.com/datasets/masoudnickparvar/brain-tumormri-dataset

We conducted a comprehensive series of ablation experi- 492 ments, aiming to validate the effectiveness of the Attention 493 Block module and Channel Mixing module in enhancing 494 super-resolution performance and model stability. 495 Our experimental setup involved a precise three-step ab- 496

Figure 4. Error Map

Table 1. Comparison on Medical Image Super-Resolution.

Method Scale Param Brain Tumor IXI PD PSNR ↑ SSIM ↑ PSNR ↑ SSIM ↑

Bicubic [2D] 2× - 26.96 0.9331 27.57 0.9523 EDSR [31] + MMHCA [14] 2× 20.8M 31.70 0.8397 32.08 0.9604 SwinIR [30] 2× 11.9M 35.60 0.9347 32.82 0.9631 MambaIR [18] 2× 22.9M 35.75 0.9362 33.30 0.9650 MambaIRv2 [19] 2× 27.6M 36.43 0.9431 33.58 0.9664 MambaNA [Ours] 2× 30.5M 36.95 0.9447 33.94 0.9686

Bicubic [2D] 4× - 18.85 0.7535 21.22 0.8293 EDSR [31] + MMHCA [14] 4× 20.8M 28.10 0.9059 28.45 0.8925 SwinIR [30] 4× 11.9M 30.23 0.9235 28.12 0.9011 MambaIR [18] 4× 22.9M 30.75 0.9202 29.56 0.9073 MambaIRv2 [19] 4× 27.6M 31.50 0.8609 30.07 0.9334 MambaNA [Ours] 4× 30.5M 32.28 0.9386 30.64 0.9379

Attention Block Channel Mixing PSNR ↑ SSIM ↑

✘ ✔ 36.41 0.9413 ✔ ✘ 36.65 0.9462 ✘ ✘ 35.68 0.8874

ing modules were simultaneously removed, representing a 505 simplified Mamba-based super-resolution architecture. All 506 ablation variants were trained and evaluated under identi- 507 cal conditions, including dataset splits, optimizer, learning 508 rate schedule, and epoch count, ensuring a fair and rigorous 509 comparison. Performance was quantified using PSNR and 510 SSIM. 511

Table 2. Ablation on the effectiveness of different components.

lation process. For the first step, the Attention Block mod- 497

ule was directly removed, allowing us to ascertain the im- 498

pact of non-causal modeling and enhanced local feature ex- 499

traction. In the second step, we removed the Channel Mix- 500

ing module in SSM-Layer, to understand its specific contri- 501

bution to channel-wise feature refinement and overall model 502

robustness. Finally, the third step involved testing a base- 503

line model, where both Attention Block and Channel Mix- 504

The results, as summarized in Table 2, clearly under- 512 score the critical and independent contribution of both the 513 Attention Block and the Channel Mixing module. Remov- 514 ing the Attention Block led to a notable performance degra- 515 dation of 1.0dB in PSNR compared to the full MambaNA 516 model. This significant drop directly validates Attention 517 Block’s pivotal role in introducing non-causal modeling and 518 enhancing local feature extraction. Similarly, ablating the 519 Channel Mixing module also resulted in a performance de- 520 crease of 0.8dB in PSNR. This confirms Channel Mixing’s 521

Table 3. Comparison on Classical Image Super-Resolution.

Method Scale Param BSDS100 Urban100 Manga109 PSNR ↑ SSIM ↑ PSNR ↑ SSIM ↑ PSNR ↑ SSIM ↑

EDSR [31] 2× 42.6M 32.32 0.9013 32.93 0.9351 39.10 0.9773 SwinIR [30] 2× 11.8M 31.63 0.9022 32.98 0.9363 38.89 0.9736 MambaIR[18] 2× 20.4M 31.57 0.9302 34.06 0.9446 40.10 0.9784 MambaIRv2 [19] 2× 22.9M 32.71 0.9046 34.88 0.9471 40.37 0.9785 MambaNA [Ours] 2× 31.5M 32.82 0.9054 35.36 0.9493 40.81 0.9871

EDSR [31] 4× 43.0M 27.68 0.7398 26.63 0.8012 30.89 0.9011 SwinIR [30] 4× 11.9M 27.78 0.7482 27.39 0.8213 31.92 0.9136 MambaIR[18] 4× 20.4M 27.90 0.7489 27.51 0.8273 32.16 0.9245 MambaIRv2 [19] 4× 23.1M 27.86 0.7498 27.72 0.8335 32.34 0.9288 MambaNA [Ours] 4× 31.5M 27.93 0.7488 28.04 0.8511 32.55 0.9382

## 5. Conclusion 534

Figure 5. MambaNA Ablation Study: Training Convergence (PSNR, SSIM). This figure shows the training curves on the Brain Tumor dataset, including “MambaNA w/o CM” (without Channel Mixing), “MambaNA w/o AB” (without Attention Block) and “MambaNA w/o AB & CM” (without both), illustrating each component’s contribution to performance and stability.

effectiveness in refining channel-wise feature representa- 522

tions by adaptively weighting frequency components. Be- 523

yond quantitative gains, the Channel Mixing module proved 524

In this paper, we successfully developed MambaNA, a 535 novel super-resolution framework tailored for medical im- 536 age reconstruction. By strategically adopting the Mamba 537 architecture for its inherent efficiency and long-range de- 538 pendency modeling, which are critical for processing high- 539 resolution and volumetric medical data. To overcome the 540 inherent limitations of Mamba’s causal sequence model- 541 ing, which restricts comprehensive non-causal spatial con- 542 text learning vital for precise 2D medical image detail re- 543 covery, MambaNA innovatively integrates both an Atten- 544 tion Block and a Channel Mixing module. The Atten- 545 tion Block effectively injects non-causal modeling capabil- 546 ities into the Mamba backbone, and the Channel Mixing 547 module significantly enhances the model’s training stabil- 548 ity, these concurrently contribute to substantial improve- 549 ments in overall performance. Extensive experiments con- 550 sistently demonstrated MambaNA’s superior performance 551 on medical image super-resolution tasks, achieving state-of- 552 the-art (SOTA) or near-SOTA levels on these benchmarks. 553 It also showed robust generalization to natural image tasks, 554 where it also reached highly competitive performance. This 555 work thus underscores the significant potential of Mamba- 556 based architectures in high-fidelity image reconstruction. 557 While promising, future work will focus on optimizing 558 MambaNA’s computational efficiency for extremely large 559 3D volumes and exploring unsupervised learning strategies 560 to reduce data dependency, thereby expanding its practical 561 utility in diverse clinical and research environments. - 562

indispensable for maintaining training stability, as Figure 5 525

vividly shows with smoother convergence and reduced os- 526

## References 563

cillations. The most substantial performance decline was 527

observed in the baseline model, which showed a 0.43dB 528

drop in PSNR compared to the full model, highlighting the 529

cumulative benefits of our design. These comprehensive re- 530

sults rigorously validate our design choices, confirming that 531

each proposed component is vital for MambaNA’s perfor- 532

[1] Anthony Bilodeau, Fr´ed´eric Beaupr´e, Julia Chabbert, Jean- 564 Michel Bellavance, Koraly Lessard, Andr´eanne Deschˆenes, 565 Renaud Bernatchez, Paul De Koninck, Christian Gagn´e, and 566 Flavie Lavoie-Cardinal. A self-supervised foundation model 567 for robust and generalizable representation learning in sted 568 microscopy. bioRxiv, pages 2025–06, 2025. 569

mance and robustness in medical image super-resolution. 533

[2] Hanting Chen, Yunhe Wang, Tianyu Guo, Chang Xu, Yiping 570

Deng, Zhenhua Liu, Siwei Ma, Chunjing Xu, Chao Xu, and 571

Wen Gao. Pre-trained image processing transformer. In Pro- 572

ceedings of the IEEE/CVF conference on computer vision 573

and pattern recognition, pages 12299–12310, 2021. 574

[3] Lihui Chen, Xiaomin Yang, Gwanggil Jeon, Marco Anisetti, 575

and Kai Liu. A trusted medical image super-resolution 576

method based on feedback adaptive weighted dense network. 577

Artificial Intelligence in Medicine, 106:101857, 2020. 578

[4] Yuhua Chen, Feng Shi, Anthony G Christodoulou, Yibin 579

Xie, Zhengwei Zhou, and Debiao Li. Efficient and ac- 580

curate mri super-resolution using a generative adversar- 581

ial network and 3d multi-level densely connected network. 582

In International conference on medical image computing 583

and computer-assisted intervention, pages 91–99. Springer, 584

## 2018. 585

[5] Yuhua Chen, Yibin Xie, Zhengwei Zhou, Feng Shi, An- 586

thony G Christodoulou, and Debiao Li. Brain mri super res- 587

olution using 3d deep densely connected neural networks. 588

In 2018 IEEE 15th international symposium on biomedical 589

imaging (ISBI 2018), pages 739–742. IEEE, 2018. 590

[6] Zheng Chen, Yulun Zhang, Jinjin Gu, Linghe Kong, Xi- 591

aokang Yang, and Fisher Yu. Dual aggregation transformer 592

for image super-resolution. In Proceedings of the IEEE/CVF 593

international conference on computer vision, pages 12312– 594

12321, 2023. 595

[7] Tao Dai, Jianrui Cai, Yongbing Zhang, Shu-Tao Xia, and 596

Lei Zhang. Second-order attention network for single im- 597

age super-resolution. In Proceedings of the IEEE/CVF con- 598

ference on computer vision and pattern recognition, pages 599

11065–11074, 2019. 600

[8] Chao Dong, Chen Change Loy, Kaiming He, and Xiaoou 601

Tang. Learning a deep convolutional network for image 602

super-resolution. In Computer Vision–ECCV 2014: 13th 603

European Conference, Zurich, Switzerland, September 6-12, 604

2014, Proceedings, Part IV 13, pages 184–199. Springer, 605

## 2014. 606

[9] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, 607

Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, 608

Mostafa Dehghani, Matthias Minderer, Georg Heigold, Syl- 609

vain Gelly, et al. An image is worth 16x16 words: Trans- 610

formers for image recognition at scale. arXiv preprint 611

arXiv:2010.11929, 2020. 612

[10] Sina Farsiu, M Dirk Robinson, Michael Elad, and Peyman 613

Milanfar. Fast and robust multiframe super resolution. IEEE 614

transactions on image processing, 13(10):1327–1344, 2004. 615

[11] Cristhian Forigua, Maria Escobar, and Pablo Arbelaez. Su- 616

performer: Volumetric transformer architectures for mri 617

super-resolution. In International Workshop on Simulation 618

and Synthesis in Medical Imaging, pages 132–141. Springer, 619

## 2022. 620

[12] William T Freeman, Thouis R Jones, and Egon C Pasztor. 621

Example-based super-resolution. IEEE Computer graphics 622

and Applications, 22(2):56–65, 2002. 623

[13] Yinghua Fu, Junfeng Liu, and Jun Shi. Tsca-net: Trans- 624

former based spatial-channel attention segmentation network 625

for medical images. Computers in Biology and Medicine, 626

[14] Mariana-Iuliana Georgescu, Radu Tudor Ionescu, Andreea- 628 Iuliana Miron, Olivian Savencu, Nicolae-C˘at˘alin Ristea, 629 Nicolae Verga, and Fahad Shahbaz Khan. Multimodal 630 multi-head convolutional attention with various kernel sizes 631 for medical image super-resolution. In Proceedings of the 632 IEEE/CVF winter conference on applications of computer 633 vision, pages 2195–2205, 2023. 634 [15] Albert Gu and Tri Dao. Mamba: Linear-time sequence 635 modeling with selective state spaces. arXiv preprint 636 arXiv:2312.00752, 2023. 637 [16] Albert Gu, Karan Goel, and Christopher R´e. Efficiently 638 modeling long sequences with structured state spaces. arXiv 639 preprint arXiv:2111.00396, 2021. 640 [17] Albert Gu, Isys Johnson, Karan Goel, Khaled Saab, Tri 641 Dao, Atri Rudra, and Christopher R´e. Combining recurrent, 642 convolutional, and continuous-time models with linear state 643 space layers. Advances in neural information processing sys- 644 tems, 34:572–585, 2021. 645 [18] Hang Guo, Jinmin Li, Tao Dai, Zhihao Ouyang, Xudong 646 Ren, and Shu-Tao Xia. Mambair: A simple baseline for im- 647 age restoration with state-space model. In European confer- 648 ence on computer vision, pages 222–241. Springer, 2024. 649 [19] Hang Guo, Yong Guo, Yaohua Zha, Yulun Zhang, Wenbo 650 Li, Tao Dai, Shu-Tao Xia, and Yawei Li. Mambairv2: Atten- 651 tive state space restoration. In Proceedings of the Computer 652 Vision and Pattern Recognition Conference, pages 28124– 653 28133, 2025. 654 [20] Yo Seob Han, Jaejun Yoo, and Jong Chul Ye. Deep residual 655 learning for compressed sensing ct reconstruction via persis- 656 tent homology analysis. arXiv preprint arXiv:1611.06391, 657 2016. 658 [21] Ali Hassani, Steven Walton, Jiachen Li, Shen Li, and 659 Humphrey Shi. Neighborhood attention transformer. In Pro- 660 ceedings of the IEEE/CVF conference on computer vision 661 and pattern recognition, pages 6185–6194, 2023. 662 [22] Jie Hu, Li Shen, and Gang Sun. Squeeze-and-excitation net- 663 works. In Proceedings of the IEEE conference on computer 664 vision and pattern recognition, pages 7132–7141, 2018. 665 [23] Shan Huang, Xiaohong Liu, Tao Tan, Menghan Hu, Xiaoer 666 Wei, Tingli Chen, and Bin Sheng. Transmrsr: transformer- 667 based self-distilled generative prior for brain mri super- 668 resolution. The Visual Computer, 39(8):3647–3659, 2023. 669 [24] Tao Huang, Xiaohuan Pei, Shan You, Fei Wang, Chen Qian, 670 and Chang Xu. Localmamba: Visual state space model with 671 windowed selective scan. In European Conference on Com- 672 puter Vision, pages 12–22. Springer, 2025. 673 [25] Robert Keys. Cubic convolution interpolation for digital im- 674 age processing. IEEE transactions on acoustics, speech, and 675 signal processing, 29(6):1153–1160, 2003. 676 [26] Jiwon Kim, Jung Kwon Lee, and Kyoung Mu Lee. Accurate 677 image super-resolution using very deep convolutional net- 678 works. In Proceedings of the IEEE conference on computer 679 vision and pattern recognition, pages 1646–1654, 2016. 680 [27] Christian Ledig, Lucas Theis, Ferenc Husz´ar, Jose Caballero, 681 Andrew Cunningham, Alejandro Acosta, Andrew Aitken, 682 Alykhan Tejani, Johannes Totz, Zehan Wang, et al. Photo- 683 realistic single image super-resolution using a generative ad- 684 versarial network. In Proceedings of the IEEE conference on 685

170:107938, 2024. 627

computer vision and pattern recognition, pages 4681–4690, 686

## 2017. 687

[28] Juncheng Li, Hanhui Yang, Qiaosi Yi, Minhua Lu, Jun Shi, 688

and Tieyong Zeng. High-frequency modulated transformer 689

for multi-contrast mri super-resolution. IEEE Transactions 690

on Medical Imaging, 2025. 691

[29] Zhen Li, Jinglei Yang, Zheng Liu, Xiaomin Yang, Gwang- 692

gil Jeon, and Wei Wu. Feedback network for image super- 693

resolution. In Proceedings of the IEEE/CVF conference on 694

computer vision and pattern recognition, pages 3867–3876, 695

## 2019. 696

[30] Jingyun Liang, Jiezhang Cao, Guolei Sun, Kai Zhang, Luc 697

Van Gool, and Radu Timofte. Swinir: Image restoration us- 698

ing swin transformer. In Proceedings of the IEEE/CVF inter- 699

national conference on computer vision, pages 1833–1844, 700

## 2021. 701

[31] Bee Lim, Sanghyun Son, Heewon Kim, Seungjun Nah, and 702

Kyoung Mu Lee. Enhanced deep residual networks for single 703

image super-resolution. In Proceedings of the IEEE confer- 704

ence on computer vision and pattern recognition workshops, 705

pages 136–144, 2017. 706

[32] Lin Lin, Jinlei Wu, Song Fu, Sihao Zhang, Changsheng 707

Tong, and Lizheng Zu. Channel attention & temporal at- 708

tention based temporal convolutional network: A dual at- 709

tention framework for remaining useful life prediction of 710

the aircraft engines. Advanced Engineering Informatics, 60: 711

102372, 2024. 712

[33] Yue Liu, Yunjie Tian, Yuzhong Zhao, Hongtian Yu, Lingxi 713

Xie, Yaowei Wang, Qixiang Ye, Jianbin Jiao, and Yunfan 714

Liu. Vmamba: Visual state space model. Advances in neural 715

information processing systems, 37:103031–103063, 2024. 716

[34] Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng 717

Zhang, Stephen Lin, and Baining Guo. Swin transformer: 718

Hierarchical vision transformer using shifted windows. In 719

Proceedings of the IEEE/CVF international conference on 720

computer vision, pages 10012–10022, 2021. 721

[35] Dwarikanath Mahapatra and Behzad Bozorgtabar. Progres- 722

sive generative adversarial networks for medical image super 723

resolution, 2019. 724

[36] Usman Muhammad and Jorma Laaksonen. Dacn: Dual- 725

attention convolutional network for hyperspectral image 726

super-resolution, 2025. 727

[37] Ozan Oktay, Wenjia Bai, Matthew Lee, Ricardo Guerrero, 728

Konstantinos Kamnitsas, Jose Caballero, Antonio de Mar- 729

vao, Stuart Cook, Declan O’Regan, and Daniel Rueckert. 730

Multi-input cardiac image super-resolution using convolu- 731

tional neural networks. In Medical Image Computing and 732

Computer-Assisted Intervention-MICCAI 2016: 19th Inter- 733

national Conference, Athens, Greece, October 17-21, 2016, 734

Proceedings, Part III 19, pages 246–254. Springer, 2016. 735

[38] Junyoung Park, Donghwi Hwang, Kyeong Yun Kim, Se- 736

ung Kwan Kang, Yu Kyeong Kim, and Jae Sung Lee. Com- 737

puted tomography super-resolution using deep convolutional 738

neural network. Physics in Medicine & Biology, 63(14): 739

145011, 2018. 740

[39] Chi-Hieu Pham, Carlos Tor-D´ıez, H´el`ene Meunier, Nathalie 741

Rousseau. Multiscale brain mri super-resolution using deep 743 3d convolutional networks. Computerized Medical Imaging 744 and Graphics, 77:101647, 2019. 745 [40] Zequn Qin, Pengyi Zhang, Fei Wu, and Xi Li. Fcanet: 746 Frequency channel attention networks. In Proceedings of 747 the IEEE/CVF international conference on computer vision, 748 pages 783–792, 2021. 749 [41] Defu Qiu, Yuhu Cheng, and Xuesong Wang. Dual u- 750 net residual networks for cardiac magnetic resonance im- 751 ages super-resolution. Computer Methods and Programs in 752 Biomedicine, 218:106707, 2022. 753 [42] Defu Qiu, Yuhu Cheng, and Xuesong Wang. Residual dense 754 attention networks for covid-19 computed tomography im- 755 ages super resolution. IEEE Transactions on Cognitive and 756 Developmental Systems, 15(2):904–913, 2022. 757 [43] Jiacheng Ruan, Jincheng Li, and Suncheng Xiang. Vm-unet: 758 Vision mamba unet for medical image segmentation. arXiv 759 preprint arXiv:2402.02491, 2024. 760 [44] Jo Schlemper, Jose Caballero, Joseph V Hajnal, Anthony N 761 Price, and Daniel Rueckert. A deep cascade of convolutional 762 neural networks for dynamic mr image reconstruction. IEEE 763 transactions on Medical Imaging, 37(2):491–503, 2017. 764 [45] Jun Shi, Qingping Liu, Chaofeng Wang, Qi Zhang, Shihui 765 Ying, and Haoyu Xu. Super-resolution reconstruction of 766 mr image with a novel residual learning network algorithm. 767 Physics in Medicine & Biology, 63(8):085011, 2018. 768 [46] Yunzhong Si, Huiying Xu, Xinzhong Zhu, Wenhao Zhang, 769 Yao Dong, Yuxing Chen, and Hongbo Li. Scsa: Exploring 770 the synergistic effects between spatial and channel attention. 771 Neurocomputing, 634:129866, 2025. 772 [47] Jimmy TH Smith, Andrew Warrington, and Scott W Linder- 773 man. Simplified state space layers for sequence modeling. 774 arXiv preprint arXiv:2208.04933, 2022. 775 [48] Henry Stark and Peyma Oskoui. High-resolution image re- 776 covery from image-plane arrays, using convex projections. 777 Journal of the Optical Society of America A, 6(11):1715– 778 1726, 1989. 779 [49] Kensuke Umehara, Junko Ota, and Takayuki Ishida. Appli- 780 cation of super-resolution convolutional neural network for 781 enhancing image resolution in chest ct. Journal of digital 782 imaging, 31:441–450, 2018. 783 [50] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszko- 784 reit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia 785 Polosukhin. Attention is all you need. Advances in neural 786 information processing systems, 30, 2017. 787 [51] Qilong Wang, Banggu Wu, Pengfei Zhu, Peihua Li, Wang- 788 meng Zuo, and Qinghua Hu. Eca-net: Efficient channel at- 789 tention for deep convolutional neural networks. In Proceed- 790 ings of the IEEE/CVF conference on computer vision and 791 pattern recognition, pages 11534–11542, 2020. 792 [52] Xintao Wang, Ke Yu, Shixiang Wu, Jinjin Gu, Yihao Liu, 793 Chao Dong, Yu Qiao, and Chen Change Loy. Esrgan: En- 794 hanced super-resolution generative adversarial networks. In 795 Proceedings of the European conference on computer vision 796 (ECCV) workshops, pages 0–0, 2018. 797 [53] Xintao Wang, Liangbin Xie, Chao Dong, and Ying Shan. 798 Real-esrgan: Training real-world blind super-resolution with 799

Bednarek, Ronan Fablet, Nicolas Passat, and Franc¸ois 742

pure synthetic data. In Proceedings of the IEEE/CVF inter- 800

national conference on computer vision, pages 1905–1914, 801

## 2021. 802

[54] Zhendong Wang, Xiaodong Cun, Jianmin Bao, Wengang 803

Zhou, Jianzhuang Liu, and Houqiang Li. Uformer: A general 804

u-shaped transformer for image restoration. In Proceedings 805

of the IEEE/CVF conference on computer vision and pattern 806

recognition, pages 17683–17693, 2022. 807

[55] Jiangwei Weng, Zhiqiang Yan, Ying Tai, Jianjun Qian, Jian 808

Yang, and Jun Li. Mamballie: Implicit retinex-aware low 809

light enhancement with global-then-local state space. arXiv 810

[66] Zou Zhen, Yu Hu, and Zhao Feng. Freqmamba: Viewing 858 mamba from a frequency perspective for image deraining. 859 arXiv preprint arXiv:2404.09476, 2024. 860 [67] Pengcheng Zheng, Kecheng Chen, Jiaxin Huang, Bohao 861 Chen, Ju Liu, Yazhou Ren, and Xiaorong Pu. Efficient med- 862 ical image restoration via reliability guided learning in fre- 863 quency domain. arXiv preprint arXiv:2504.11286, 2025. 864 [68] Lianghui Zhu, Bencheng Liao, Qian Zhang, Xinlong Wang, 865 Wenyu Liu, and Xinggang Wang. Vision mamba: Efficient 866 visual representation learning with bidirectional state space 867 model, 2024. 868

preprint arXiv:2405.16105, 2024. 811

[56] Jelmer M Wolterink, Tim Leiner, Max A Viergever, and 812

Ivana Iˇsgum. Generative adversarial networks for noise re- 813

duction in low-dose ct. IEEE transactions on medical imag- 814

ing, 36(12):2536–2545, 2017. 815

[57] Rui Xu, Shu Yang, Yihui Wang, Yu Cai, Bo Du, and Hao 816

Chen. Visual mamba: A survey and new outlooks. arXiv 817

preprint arXiv:2404.18861, 2024. 818

[58] Chenhongyi Yang, Zehui Chen, Miguel Espinosa, Linus Er- 819

icsson, Zhenyu Wang, Jiaming Liu, and Elliot J Crowley. 820

Plainmamba: Improving non-hierarchical mamba in visual 821

recognition. arXiv preprint arXiv:2403.17695, 2024. 822

[59] Guang Yang, Simiao Yu, Hao Dong, Greg Slabaugh, 823

Pier Luigi Dragotti, Xujiong Ye, Fangde Liu, Simon Arridge, 824

Jennifer Keegan, Yike Guo, et al. Dagan: deep de-aliasing 825

generative adversarial networks for fast compressed sensing 826

mri reconstruction. IEEE transactions on medical imaging, 827

37(6):1310–1321, 2017. 828

[60] Qingsong Yang, Pingkun Yan, Yanbo Zhang, Hengyong Yu, 829

Yongyi Shi, Xuanqin Mou, Mannudeep K Kalra, Yi Zhang, 830

Ling Sun, and Ge Wang. Low-dose ct image denoising using 831

a generative adversarial network with wasserstein distance 832

and perceptual loss. IEEE transactions on medical imaging, 833

37(6):1348–1357, 2018. 834

[61] Chenyu You, Wenxiang Cong, Michael W. Vannier, 835

Punam K. Saha, Eric A. Hoffman, Ge Wang, Guang Li, 836

Yi Zhang, Xiaoliu Zhang, Hongming Shan, Mengzhou Li, 837

Shenghong Ju, Zhen Zhao, and Zhuiyang Zhang. Ct super- 838

resolution gan constrained by the identical, residual, and cy- 839

cle learning ensemble (gan-circle). IEEE Transactions on 840

Medical Imaging, 39(1):188–203, 2020. 841

[62] Hanwei Zhang, Ying Zhu, Dan Wang, Lijun Zhang, Tianx- 842

iang Chen, Ziyang Wang, and Zi Ye. A survey on visual 843

mamba. Applied Sciences, 14(13):5683, 2024. 844

[63] Kai Zhang, Wangmeng Zuo, Yunjin Chen, Deyu Meng, and 845

Lei Zhang. Beyond a gaussian denoiser: Residual learning of 846

deep cnn for image denoising. IEEE transactions on image 847

processing, 26(7):3142–3155, 2017. 848

[64] Yulun Zhang, Yapeng Tian, Yu Kong, Bineng Zhong, and 849

Yun Fu. Residual dense network for image super-resolution. 850

In Proceedings of the IEEE conference on computer vision 851

and pattern recognition, pages 2472–2481, 2018. 852

[65] Can Zhao, Muhan Shao, Aaron Carass, Hao Li, Blake E 853

Dewey, Lotta M Ellingsen, Jonghye Woo, Michael A 854

Guttman, Ari M Blitz, Maureen Stone, et al. Applications of 855

a deep learning method for anti-aliasing and super-resolution 856

in mri. Magnetic resonance imaging, 64:132–141, 2019. 857
