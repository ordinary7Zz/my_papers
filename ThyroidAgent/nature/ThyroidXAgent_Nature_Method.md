\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{imgs/ThyroidXAgent_for_seg_and_cls.png}
\caption{Overview of ThyroidXAgent for segmentation and classification. Evidence-aware routing integrates lesion delineation, malignancy assessment and radiomic interpretation under heterogeneous acquisition settings.}
\label{fig:ThyroidXAgent_for_seg_and_cls}
\end{figure}

\subsection{ThyroidXAgent for Segmentation and Classification}
As shown in Fig.~\ref{fig:ThyroidXAgent_for_seg_and_cls}, ThyroidXAgent combines lesion segmentation, malignancy classification and radiomic feature extraction within a single workflow. The segmentation and classification branches share a DINOv3-based backbone~\cite{simeoni2025dinov3} with task-specific lightweight heads. For segmentation, we use a U-Net-style decoder with skip fusion to produce a dense nodule mask probability map, optimized with a weighted BCE+IoU loss. For classification, global average- and max-pooled backbone features are passed to a compact attention-based head to estimate malignancy probability, trained with a GLA loss to mitigate class imbalance. The radiomics branch extracts 2D PyRadiomics descriptors~\cite{van2017computational} from the selected lesion mask and provides complementary shape and texture measurements for downstream tabular modelling.

At inference, candidate masks and class predictions are evaluated together with imaging metadata describing the acquisition setting, including scanner provenance and input resolution. The final output is selected according to its consistency with these signals rather than by raw confidence alone. The selected lesion mask is then used for radiomic feature extraction, and the resulting features are passed to an AutoGluon-based tabular classifier~\cite{erickson2020autogluon}. SHAP~\cite{lundberg2017unified} was used to summarize feature contributions for interpretation.
