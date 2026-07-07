# arXiv:2601.17151v1 [cs.CV] 23 Jan 2026

## Scalingmedicalimagingreportgenerationwith

## multimodalreinforcementlearning

#### QianchuLiu∗,ShengZhang∗,GuanghuiQin∗,

#### YuGu,YingJin,SamPreston,YanboXu,SidKiblawi, Wen-waiYim,TimOssowski,TristanNaumann,MuWei†,HoifungPoon†

#### MicrosoftResearch

## Abstract

Frontiermodelshavedemonstratedremarkablecapabilitiesinunderstandingandreasoningwith natural-languagetext,buttheystillexhibitmajorcompetencygapsinmultimodalunderstandingand reasoningespeciallyinhigh-valueverticalssuchasbiomedicine.Medicalimagingreportgenerationisa prominentexample.Supervisedfine-tuningcansubstantiallyimproveperformance,buttheyareproneto overfittingtosuperficialboilerplatepatterns.Inthispaper,weintroduceUniversalReportGeneration (UniRG)asageneralframeworkformedicalimagingreportgeneration.Byleveragingreinforcement

learningasaunifyingmechanismtodirectlyoptimizeforevaluationmetricsdesignedforendapplications, UniRGcansignificantlyimproveuponsupervisedfine-tuningandattaindurablegeneralizationacross diverseinstitutionsandclinicalpractices.WetrainedUniRG-CXRonpubliclyavailablechestX-ray (CXR)dataandconductedathoroughevaluationinCXRreportgenerationwithrigorousevaluation

scenarios.On the authoritative ReXrank benchmark,UniRG-CXR sets new overall SOTA, outperforming priorstateoftheartbyawidemargin.

### Main

Medicalimagingreportgenerationhasbeenanimportantapplicationareaformedicalfoundationmodels, aiming to automatically produce coherent and clinically meaningful diagnostic reports from medical images such as chest radiographs.Beyond its potential to reduce reporting burden, improve workflow efficiency, and enhance diagnosticconsistency,reportgenerationrepresentsakeybenchmarkforevaluatingbroadermultimodal reasoningcapabilitiesinhealthcareAI.Despiterecentprogressdrivenbylarge-scalevision–languagemodels anddomain-specifictrainingcorpora[17,26,32],enablingmodelstoproducefaithful,clinicallygrounded reportsthatgeneralizeacrossreal-worldimagingenvironmentsremainsasubstantialchallenge.

Acentralobstacleliesincross-institutiongeneralization.Forexample,radiologyreportingpractices varywidelyacrossdatasetsandhealthcaresystems,influencedbydifferencesininstitutionalguidelines, departmentalconventions,radiologistwritingstyles,andpatientpopulations[5].Consequently,models trainedthroughsupervisedfine-tuning(SFT)tendtoinheritthelexicalbiases,phrasingpatternsoftheir trainingdatasets.Whilesuchmodelsmayachievehighscoresonin-distributionbenchmarks,theyoften showsubstantialdegradationwhenevaluatedonunseeninstitutionsorexternaldatasets.Thisbrittlenessis particularlyconcerningforsafety-criticalapplications,wherereliableperformanceacrossdemographicgroups, institutions,andimagingconditionsisessential.

AsecondmajorlimitationofpriorworkisthatSFTobjectivesprimarilyoptimizenext-wordprediction, whichencouragessurface-levellexicalsimilaritytoreferencereportsratherthanalignmentwithclinically important factual attributes.As a result, conventional report generation systems often overfit to n-gram–based metrics(e.g.,BLEU,ROUGE)thatareonlyweaklycorrelatedwithradiologicalcorrectness[22,26].This misalignmenthighlightstheneedfortrainingparadigmsthatoptimizemodelsdirectlyforclinicalusefulness andfactualaccuracyratherthansuperficiallinguisticsimilarity.

#### ∗Equalcontributions †Correspondingauthors:muhsin.wei@microsoft.com,hoifung@microsoft.com

Toaddressthesechallenges,weintroduceUniRG,aunifiedanduniversalreportgenerationframework builtuponanovelreinforcementlearningframeworkdesignedtoenhancegeneralization,factualalignment, androbustness.OurRLstrategydirectlyoptimizesclinicallygroundedrewardsignalsthatcapturediseasespecificcorrectness,structuredfactualrelationships,andmulti-metricperformance.Usingthisframework, wetrainUniRG-CXRonchestX-raysandshowthatitmovesbeyonddataset-specificreportingconventions, instead learning generalizable representations that yield consistently strong performance across diverse clinical settings.

WeconductextensiveandrigorousevaluationstobenchmarkUniRG-CXRagainstexistingradiology reportgenerationmodelsacrossabroadspectrumofsettings.Ourevaluationsuiteincludesstandard report-levelgenerationmetrics,condition/diesease-levelclassification,cross-dataset/institution/demographics generalization,andlongitudinalevaluationreflectingreal-worldclinicalpractices.Acrossallaxes,UniRG- CXRachievesoverallstate-of-the-art(SOTA)performance,consistentlysurpassingpriorbaselinesand demonstratinguniversal,reliablecapabilitiesrarelyobservedinpriorRRGsystems.

Insummary,ourcontributionsarethreefold: Anewreinforcementlearningframework(UniRG)forradiologyreportgeneration,yielding UniRG-CXR,asinglemodelthatattainsoverallSOTAperformanceacrossmultipledatasetsandevaluation metrics.

Acomprehensive,clinicallygroundedevaluationofUniRG-CXR,spanningreport-levelmetrics,disease-levelcorrectness,cross-datasetandcross-institutiongeneralization,robustnessanalyses,and longitudinalassessment.

DemonstrationofUniRG-CXR’suniversalcapabilities,showingthatUniRG-CXRovercomesthe longstandingspecializationandmetric-overfittingissuesofSFT-basedreportgenerationmodelsbyproducing clinicallyaligned,generalizablereportsacrossdiversereal-worldconditions.

Together,theseadvancesestablishUniRGasarobustandgeneralizablefoundationforradiologyreport generationandhighlightthepromiseofreinforcementlearningasakeycomponentofnext-generationclinical vision–languagemodels.

## Results

#### OverviewofUniRGandUniRG-CXR

WeproposeUniRG,anext-generationapproachformedicalimagingreportusingreinforcementlearning. Withthisframework,wetrainUniRG-CXR,astate-of-the-artmodelforradiologyreportgenerationthat

producesclinicallyfaithfulreportsacrossdiverseinstitutionsanddatasetswithsubstantialleadoverexisting baselines.Builtupontheopen-sourceQwen3-VL-8B-Instructfoundation,UniRG-CXRcombinedsupervised fine-tuningwithreinforcementlearningtodirectlyoptimizeforclinicallyrelevantobjectiveaggregating multiplemetricsspanningrule-based(BLEU),model-based(BERTScore,SembScore,RadGraphF1),and LLM-based(CheXprompt)metrics.Trainedonlarge-scaledatasetsincludingMIMIC-CXR,CheXpertPlus, ReXGradientandIU(coveringover560kstudiesfrom80+institutions),UniRG-CXRcanconditiononthe currentimage,contextualtext,andpriorstudyinformationwhereavailableandoutputbothfindingsand impression as a full radiology report from the x-ray interpretation.To evaluate the quality ofUniRG-CXR, we assess UniRG-CXR on held-out test sets (MIMIC-CXR [11], CheXpert Plus [4], ReXGradient [30], IU [6]) and unseenproprietarydata.ReportqualityismeasuredusingReXrankmetrics[29]andCheXprompt,anLLMbasedclinical-errormetric[27],whilediagnosticabilityisevaluatedviaF1-baseddiseaseclassificationfrom generatedreports.UniRG-CXRdemonstratesunprecedentedgeneralizationandrobustness,outperforming priorstate-of-the-artsystems(e.g.,MedVersa,MedGemma,MAIRA-2)bysubstantialmarginsacrosspublic andprivatebenchmarksacrossourevaluationsettings.

Asshownin(d)and(e)fromFigure2,wepresentthedetailedReXrankleaderboardresults1which compares UniRG-CXR against previous SOTA models across four datasets—ReXGradient [30], MIMIC-CXR [11],IUX-Ray[6],andCheXpertPlus[4].Eachdatasetisevaluatedundertwogenerationsettings:findingsonlyandthemorechallengingfindings+impressionsetup.Performanceismeasuredby1/RadCliQ-v1 [24](higherisbetter),acompositemetricusedasthedefaultmetricinRexRankleaderboardandwas

#### 1ResultsarecollectedfromtheReXrankleaderboard[29]

#### (a) (b)

#### Study i Study i -1

Context

#### Training Data

#### sexage indication ···

#### ······

#### 229,161 patients 563,494 studies 785,687 images

Time

(longitudinal input)

#### Over 80 medical institutions

#### Institution

#### UniRG-CXR

#### Vision encoder

CheXpert Plus

#### Dataset

40% MIMIC-CXR

33% ReXGraident

26%

#### Language model

emergency

#### Department

34% in/outpatient

66%

maie

#### Sex

37% female

29% unknown

34%

Rule-based rewards Rule-based rewards Rule-based rewards Model-based rewards Model-based rewards Rule-based rewards Rule-based rewards Model-based rewards LLM-based rewards

unknown

#### Race

4% white

23%

2% asian

71% black

#### Reward aggregator

#### xN

#### Age

35% 80+ 10%

0-20 4% 20-40 10% 40-60 19% 60-80 22% unknown

#### GRPO

#### Held-out test data

#### (c)

#### ReXrank

#### Report-level

#### metrics

#### evaluation

#### UniRG-CXR

Cardiomegaly

#### Clinical

#### Unseen external data

Pleural Effusion

#### errors

#### Text-based

Lung Opacity

#### classiﬁer

#### ···

Atelectasis

#### F1 scores

#### Disease-level evaluation

Findings: There are low lung volumes... There is evidence of trace pulmonary edema with a left pleural effusion. Left retrocardiac atelectasis is noted. There are old bilateral rib fractures. Impression: 1. TRACE PULMONARY EDEMA WITH LEFT PLEURAL EFFUSION. 2. LOW LUNG VOLUMES A ND LEFT LOWER LOBE ATELECTASIS. 3. OLD BILATERAL RIB FRACTURES

### ReXGradient

### MIMIC-CXR

### IU Xray

### CheXpert Plus

#### (d)

1.7

### 4.8 4.80

### 1.20 1.16

1.62

### 1.30 1.23

1.05

1.4

1.35

1.12

1.02

3.4

### 1.10 1.061.03

1.12

### Findings

1.1

2.0

0.93

0.83

#### 0.860.85 0.810.800.79

### 1/RadCliQ-v1

0.900.890.87

1.021.011.010.96

### 1.92 1.671.461.461.381.34

0.8

0.75

0.6

0.65

Libra

VLCI-IU

MAIRA-2

MAIRA-2

MedVersa

MedVersa

MedVersa

MoERad-IU

MoERad-IU

MedGemma

MedGemma

UniRG-CXR

UniRG-CXR

UniRG-CXR

UniRG-CXR

CheXOne-R1

CheXOne-R1

CheXOne-R1

CheXOne-R1

CXRMate-ED

RadPhi3.5Vision

RadPhi3.5Vision

CXRMate-RRG24

CXRMate-RRG24

CXP+CheX-MIMIC

RadPhi4VisionCXR

RadPhi4VisionCXR

RadPhi4VisionCXR

### 5.2 5.14

1.59

1.6

### 1.15 1.07

### 0.75 0.70 0.68

1.3

0.920.91

0.62

3.6

0.93

0.820.80

0.71

0.9

0.72

2.0

0.48

#### 0.510.510.490.48 0.44

### 1/RadCliQ-v1

#### 0.980.93 0.840.790.750.74

0.62

1.451.251.221.111.040.99

### Findings + Impression

0.5

0.50

0.4

0.35

RadFM

RadFM

RadFM

RadFM

MedVersa

MedVersa

MedVersa

MedVersa

CXP+CheX

CXP+CheX

CXP+CheX

CXP+CheX

UniRG-CXR

UniRG-CXR

UniRG-CXR

UniRG-CXR

CXP+MIMIC

CXP+MIMIC

CXP+MIMIC

CXP+MIMIC

CheXOne-R1

CheXOne-R1

CheXOne-R1

CheXOne-R1

CXP+CheX-MIMIC

CXP+CheX-MIMIC

CXP+CheX-MIMIC

CXP+CheX-MIMIC

Figure1:OverviewofUniRG-CXR.(a)TrainingData:UniRG-CXRistrainedonthetrainingsplitsofMIMIC- CXR[11],CheXpertPlus[4],ReXGradient-160k[30]andIU[6]coveringdiverseinstitutionsandpatientdemographics. (b)TrainingandRewards:Takinginputfromthecurrentimage,clinicalcontext(e.g.,indication),andoptionallyprior

studies,UniRG-CXRusesGRPOreinforcementlearningtooptimizecompositerewardsthatcombinerule-based, model-based, and LLM-based metrics.(c) Evaluation:We assess UniRG-CXR on held-out test sets from MIMIC-CXR, CheXpertPlus,ReXGradientandadditionallyassesszero-shotgeneralizationonanexternalproprietarydataset andIU-Xray(thezero-shotsettingexcludesIU-Xraytrainingdata).ReportqualityismeasuredusingReXrank metrics[29]andanLLM-basedclinical-errormetric[27],whilediagnosticabilityisevaluatedviaF1-baseddisease classificationfromgeneratedreports.(d)ReXrankResults:UniRG-CXRachievesSOTAperformanceacrossfour datasetsandtwogenerationsettings(findingsonlyandfindings+impression),showingsubstantialgainsoverprior state-of-the-art.

foundtocorrelatemorestronglywithhumanjudgmentthanindividualmetrics.AsshowninFigure1, UniRG-CXRachievesconsistentandsubstantialgainsoverpriorSOTAmodelsineverysteup.Notably,on theReXGradientandIUtestset,UniRG-CXRexceedsthepreviousbestmodelbyover50%,underscoring itsstronggeneralizationcapabilityforradiologyreportgeneration.

#### UniRG-CXRachievesSOTAwithuniversalimprovementsacrossmetrics

#### WhileRadCliQ-v1servesasourprimaryevaluationmetric,Figure2furtherillustratesthatUniRG-CXR

deliversbroadimprovementsacrossdiversemetricsincludingboththoseemphasizinglexicalsimilarity(e.g., BLEU, BERTScore) and those emphasizing factual correctness (e.g., SembScore).Notably, UniRG-CXR also improvesmetricsitwasnotexplicitlyoptimizedfor,suchasRaTEScore,highlightingthatitsperformance gainsareuniversalandmulti-facetedratherthanoverfittedtospecificmetrics(Figure2(a)).Thekeytothis universalimprovementsliesinourcombinedrewardRLwhichjointlyoptimizesmultipleindividualmetrics. AsshowninFigure2(b)and(c),wecompareUniRG-CXRwithablationstudiesthatonlyoptimizean individualmetric.WeshowthatourproposedcombinedrewardRLachievesbalancedgainsacrossindividual metricsandyieldsoverallthebestRadCliQ-v1score.

BeyondtheReXrank-providedmetrics,weadditionallyevaluateUniRG-CXRusingCheXprompt[27], anLLM-basedmetricthatquantifiesthenumberofclinicalerrorsrelativetothereferencereport(following ZambranoChavesetal.[27],weuseGPT-4asthebackboneevaluator).AsshowninFigure2(f),we comparetheproportionofgeneratedreportswithvaryingnumbersofclinicalerrors(≤1,2,3,and≥4) acrossUniRG-CXR,MedVersa,andMedGemma.UniRG-CXRproducessubstantiallymoreerror-freeor low-errorreports(21.3%≤1error)comparedwithpriorstate-of-the-artsystems(Medversa16.1%and MedGemma3.1%),whilemarkedlyreducingthefractionofhigh-errorreports(≥4errors:14.8%)relative toMedVersa(32.3%)andMedGemma(43.5%).TheseresultsindicatethatUniRG-CXRachievesmore clinicallyfaithfulandaccuratereportgeneration.Qualitatively,weshowanexamplewhereUniRG-CXR cangenerateerror-freereportthatcoversalltheimportantfindingswhileoutputfromMedGemmaand MedVersacontainerrorsorpartialerrors.Thekeytotheimprovementonclinicalerrorreductionisthe incorporationoferrorawarenessmetric(i.e.CheXprompt)inourcombinedRLrecipeinUniRG-CXR.In Figure2(d),theRL(noerrorawareness)ablationthatdoesnotcontainCheXpromptoptimizationshows stagnantlearningintermsofreducingclinicalerrorswhereasourfullRLrecipefromUniRG-CXRthat incorporateserrorawarenessleadstoasteadydownwardtrajectoryofreductioninreporterrorsthroughout training,indicatingthatexplicitoptimizationforclinicalcorrectnesseffectivelyimprovesreportfidelity.

#### UniRG-CXRenhanceslongitudinalreportgeneration

Inthereal-worldsetting,radiologistsroutinelyreferencepriorstudies(bothreportsandimages)when interpretingthecurrentexam,oftennotingchangessuchaswhetherpneumoniahasimprovedorworsened comparedtoapreviousscan.Tobetterapproximatethisrealisticworkflow,weincorporatelongitudinal training, enabling the model to condition on both the prior image and prior report, during the RL training.As showninFigure3,UniRG-CXRachievesthebestperformanceinlongitudinalreportgenerationcompared withpriorlongitudinalreportgenerationmodelssuchasMaira-2andfrontierlargelanguagemodelsuch asGPT-5.WealsonoticethatlongitudinalinformationiseffectivelyincorporatedinUniRG-CXRasit boostsperformanceoveritsnon-longitudinalsetup.TounderstandthegainofUniRG-CXRinmore granularity,wefurthercategorizethereportsasshowninFigure3(b).TheteststudiesfromMIMICare splitintofivecategoriesaccordingtotheirencountertimepointsrangingfromfirstencounterreportwithout priorinformationtoincreasedcomplexityin2nd,3rd,4thand5th+encounterpointswherethereportis writteninreferencewithmultipleencountersthepatienthasexperiencedinthehistory.Weobservethat thefirst-encounterreportsaregenerallythemostchallenging,andasthenumberofencountersincreases, reportqualityimprovesconsistently.Thistrendisintuitive:forthefirstencounter,themodelmustgenerate acompletelynewdescriptionbasedsolelyonthecurrentimage,withoutanypriorcontext.Incontrast, subsequentencountersprovidepreviousreportsthatcapturethepatient’sunderlyingconditions,enablingthe modeltogeneratemoreaccurateandcontextuallyfaithfulreports.Acrossallencounterpoints,UniRG-CXR achievessubstantialperformancegainsoverpriormodels.Moreover,UniRG-CXRsignificantlyoutperforms the“copypriorreport”baseline,demonstratingthatiteffectivelyleveragespriorinformationratherthan

#### (a)

#### ReXGradient

#### MIMIC-CXR

#### IU Xray

#### CheXpert Plus

1/RadCliQ-v1

1/RadCliQ-v1

1/RadCliQ-v1

1/RadCliQ-v1

4.80

1.23

1.62

1.16

BLEU

RaTEScore

BLEU

RaTEScore

BLEU

RaTEScore

BLEU

RaTEScore

0.73

0.29

0.58

0.62

0.38

0.60

0.26

0.22

#### Findings

0.26

0.27

0.54

0.64

0.49

0.45

0.30

0.40

BertScore

BertScore

BertScore

BertScore

RadGraph

RadGraph

RadGraph

RadGraph

0.70

0.53

0.58

0.50

SembScore

SembScore

SembScore

SembScore

1/RadCliQ-v1

1/RadCliQ-v1

1/RadCliQ-v1

1/RadCliQ-v1

5.14

1.59

1.07

0.70

BLEU

RaTEScore

BLEU

RaTEScore

BLEU

RaTEScore

BLEU

RaTEScore

0.30

0.72

0.57

0.61

0.61

0.40

0.17

0.20

0.18

0.18

0.27

0.40

0.42

0.53

0.64

0.30

BertScore

BertScore

BertScore

BertScore

RadGraph

RadGraph

RadGraph

RadGraph

0.52

0.57

0.49

0.70

#### Findings + Impression

SembScore

SembScore

SembScore

SembScore

#### UniRG-CXR MoERad-IU

#### Libra MedGemma

#### MAIRA-2 RadFM

#### MedVersa CheXpertPlus-CheX-MIMIC

#### (b) (c) (d)

#### RL (full) RL (no error awareness) BLEU SembScoreRadgraph1/RadCliQ-v1

#### 1.95

#### SFT baseline

#### 0.0% 0.0% 0.0% 0.0%

#### +14%

#### 1.9

#### 1.90

#### +12%

#### 1.8

#### + BLEU RL

#### +13.2% +2.1% +12.3% +7.2%

#### +10%

#### 1.85

#### 1.7

#### +8%

#### 1.80

#### + SembScore RL

#### -1.6% +15.7% 0.0% +5.1%

#### +6%

#### 1/RadCliQ-v1

#### 1.75

#### 1.6

#### # errors per report

#### +4%

#### -2.1% +3.5% +9.7% +6.1%

#### + RadGraph RL

#### 1.70

#### 1.5

#### +2%

#### RL (full) RL (BLEU only)

#### 1.65

#### Combined reward RL

#### 0%

#### +5.3% +12.2% +13.1% +15.3%

#### (UniRG-CXR)

## 0 100 200

## 0 100 200

#### -2%

#### Training Steps

#### Training Steps

#### (e)

#### (f)

## 1 error 2 errors 3 errors 4+ errors

Correct Incorrect Partially correct

#### 21.3% 32.8% 31.1% 14.8%

#### UniRG-CXR

UniRG-CXR: A right internal jugular central venous catheter now terminates in the lower SVC. There are low lung volumes. There is no pneumothorax. There is no focal consolidation or pleural effusion.

#### 16.1% 21.0% 30.6% 32.3%

#### MedVersa

MedVersa: A portable frontal chest radiograph demonstrates repositioning of the right internal jugular catheter, which now terminates in the mid SVC. The remainder of the exam is unchanged, including low lung volumes and mild elevation of the right hemidiaphragm.

#### 8.1% 21.0% 27.4% 43.5%

#### MedGemma

Context: Age: 20-30. Gender: F. Indication: Hyperglycemia and fatigue. Comparison: Chest radiograph from ___.

MedGemma: The right internal jugular central venous catheter is now positioned in the superior vena cava. There is no evidence of pneumothorax. The lungs are clear. The heart size is normal. The mediastinum is normal in width. The bony structures are intact.

Figure2:UniRG-CXRachievesstate-of-the-artperformance,deliveringconsistentandcomprehensiveperformance gainsacrossmetrics.(a)OntheReXrankleaderboard,UniRG-CXR(green)showsrobust,universalimprovement acrossallevaluationmetrics.(b).StartingfromthesameSFTcheckpoint,RLwithourcombinedrewardachieves morebalancedgainsacrossmetricsandthehighestRadCliQ-v1scorecomparedtoRLonsinglemetrics.Thisablation studyistrainedandtestedonMIMIC(c).AblationstudyonthetrainingdynamicsshowsRLfull(UniRG-CXR) achievessignificantlybetterRadCliQ-v1scorethanRLonlyonBLEU.(d).Duringtraining,RLfull(UniRG-CXR) showsasteadydecreaseinclinicalerrorsperreportascomparedwithafluctuatingtrajectorywithoutconsistent improvementfromanablationrunwithouterrorawareness(i.e.removingCheXpromptmetricoptimization).Both (c)and(d)showresultson1024MIMICvalidationsetfromablationsthataretrainedonMIMIC.(e).Casestudies

illustratethatUniRG-CXRcanproduceerror-freereports,unlikeMedVersaandMedGemma.(f).UniRG-CXR yieldsasubstantiallyhigherproportionofreportswith≤1errorandfewerwith≥4errorsthanpriormodels.

relyingonitasashortcut,abehaviorobservedinsomecompetingmodels(e.g.,MedGemma,GPT-4o,and GPT-5)whichonlymarginallyexceedthecopy-priorbaseline.Aslongitudinalreportgenerationinvolves capturing temporal changes in disease state across patient encounters.In Figure 3(c), we categorize each report intofivetemporaldescriptiontypes(firststudy(nopriorstudy),newdevelopment,nochange,progression,

#### (a)

#### UniRG-CXR Maira-2 MedGemma GPT-4o GPT-5 Copy Prior (b)

#### UniRG-CXR

#### 1.4

#### UniRG-CXR (w/o longitudinal)

#### 1.3

#### Maira-2

#### 1.2

#### 1.1

#### Maira-2 (w/o longitudinal)

#### 1.0

#### GPT-5

#### 1/RadCliQ-v1

#### 0.9

#### MedGemma

#### 0.8

#### GPT-4o

#### 0.7

### 0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4

#### 1st (n=810)

#### 2nd (n=461)

#### 3rd (n=303)

#### 4th (n=221)

#### 5th+ (n=552)

#### 1/RadCliQ-v1

#### Longitudinal Encounter

#### (c)

Conext: Age:50-60.Gender:M.Indication: ... question pneumonia, pneumothorax...

MedGemma

#### First study

No prior report

GPT-5

#### (n=810)

No prior-study

Maira-2

view

Gold: ... Tracheostomy tube is present ... There is no pneumothorax or pleural effusion. There is a hazy veil-like opacity in the right upper lung zone ... Heart size appears enlarged ...

#### ****

UniRG-CXR

Initial imaging examination for the current clinical episode.

UniRG-CXR: ... There is opacity in the right lung. There is no pneumothorax or pleural effusion. The heart is enlarged. A tracheostomy tube is in place ...

### 0.8 1.0 1.2 1.4 1.6

1/RadCliQ-v1

Conext: Age:20-30.Gender:M.Indication: Chest pain after recent fall...

MedGemma

#### New development

GPT-5

Prior report: ... no focal consolidation, pneumothorax or pleural effusion.The lungs are hyperinflated ... no free air under the right hemidiaphragm ...

#### (n=275)

Maira-2

Gold: In the left mid lung is a 2.9 cm rounded opacity with an air-fluid level concerning for a cavitary lesion. This was no present in the prior exam ...

#### ****

UniRG-CXR

A new abnormality has appeared that was not seen previously.

UniRG-CXR: ... There is a new opacity in the left mid lung. The cardiomediastinal and hilar contours are normal ...

### 0.8 1.0 1.2 1.4 1.6

1/RadCliQ-v1

Conext: Age:60-70.Gender:F.Indication:Pneumonia, evaluation for interval change.

MedGemma

#### No change

GPT-5

Prior report: ... slightly rotated positioning ... opacification of the right lung ... There may be some volume loss on the right ...

#### (n=744)

Maira-2

Gold: As compared to the previous radiograph, there is no relevant change. Extensive right pleural effusion...

#### ****

UniRG-CXR

No significant difference compared to the prior study.

UniRG-CXR: As compared to the previous radiograph, there is no relevant change. The extensive right pleural effusion with volume loss in the right lung is unchanged ...

1/RadCliQ-v1 0.8 1.0 1.2 1.4 1.6

MedGemma

#### Progression

Conext: Age:40-50.Gender:M.Indication: History of cirrhosis with TIPS and thoracentesis ... complicated by pneumothorax. Comparison: Multiple priors ...

GPT-5

#### (n=258)

Prior report: ... right-sided pneumothorax is slightly smaller. There has, however, been interval enlargement of the right-sided pleural effusion ...

Maira-2

#### ****

Gold: ... there has been continued increase in the pleural effusion which is now large and leaving only the right upper lobe aerated ...

UniRG-CXR

The abnormality has increased in size, extent, or severity.

UniRG-CXR: There has been interval increase in the large right pleural effusion. There is a small right pneumothorax. The left lung is clear ...

### 0.8 1.0 1.2 1.4 1.6

1/RadCliQ-v1

MedGemma

Conext: Age:70-80.Gender:M.Indication: ... recurrent right pleural effusion status post thoracentesis. Evaluate for pneumothorax or reexpansion ...

#### Regression

GPT-5

#### (n=260)

Prior report: ... There is a stable moderate layering right pleural effusion since___... There is no evidence of pneumothorax ...

Maira-2

Gold: There has been mild interval decrease of a still moderate right pleural effusion ... There is no evidence of pneumothorax ...

#### ****

UniRG-CXR

The abnormality has decreased but not fully resolved.

UniRG-CXR: There has been interval decrease in the right moderate pleural effusion. There is no pneumothorax ...

### 0.8 1.0 1.2 1.4 1.6

1/RadCliQ-v1

Figure3:UniRG-CXRenhanceslongitudinalreportgeneration.(a).ComparingUniRG-CXRanditsnonlongitudinalablationwithpriormodelsonlongitudinalreportgeneration,weshowUniRG-CXRexhibitsthebest performanceandthelongitudinalinformationisbeneficialtotheperformance.(b).UniRG-CXRachievesthebest performanceacrossdifferentlongitudinalencounterpointsrangingfromthefirstencountertothemorecomplex5th+ encounters,showcasingitsimprovementsareacrosstheboard.Incomparison,priormodelssuchasGPT-5,GPT-4o andMedGemmaarebarelysurpassingthecopypriorreportbaseline(greylines).(c).Comparedwithpriormodels whichbarelyimproveoverthecopypriorbaseline(dashedline),UniRG-CXRsignificantlyandconsistentlyimproves performanceacrossdifferenttemporaldiseasechangecategoriesincludingnewdevelopment,nochange,progression andregression(categorizedbyGPT-5ongroundtruthreport).Qualitativeexamplesareshownforeachcategory whereUniRG-CXRcorrectlypredictsthetemporalchangebasedontheinput.AllresultsinthisfigureareonMIMIC testsetwithpriorinformationwhereavailable.

andregression)usingGPT-5asanautomaticlabeler.WeevaluateUniRG-CXR’sperformanceacross thesecategories,comparingitagainstpriormodelsandthecopypriorreportbaseline.Asexpected,theno

changecategoryistheeasiest,sincemuchofthecontentcanbereusedfromthepriorreport.Incontrast, categoriesreflectingdiseaseevolutionsuchasregressionornewdevelopmentaremorechallenging,asthe modelmustaccuratelylocalizeandquantifysubtlechanges.UniRG-CXRdemonstratesconsistentand substantialimprovementsacrossallcategories,markedlysurpassingbothpriormodelsandthecopy-prior baseline.QualitativeexamplesfurtherillustratethatUniRG-CXRgeneratesclinicallyfaithfullongitudinal descriptions,correctlyidentifyingchangessuchasnewfindingsorresolvingabnormalities.Collectively, theseresultshighlightUniRG-CXR’ssuperiorcapabilitytomodelandreasonoverlongitudinalpatient trajectories.

#### GeneralizationandRobustnessofUniRG-CXR

#### BLEU

#### BERTScore

#### SembScore

#### RadGraph

#### 1/RadCliQ-v1

#### (a)

#### UniRG-CXR

#### MedGemma

#### MedVersa

#### IU-Xray

#### GPT-5

#### GPT-4o

## 0 10 20

## 0 20 40 60

## 0 20 40 60

## 0 10 20 30

## 0 1 2

#### UniRG-CXR

#### MedGemma

#### MedVersa

#### GPT-5

#### Proprietary Data

#### GPT-4o

## 0 10 20

## 0 20 40 0 20 40 0 10 20 0.0 0.5 1.0

#### (b) (c)

#### Cardiomegaly

#### No Finding

#### (n=1026)

#### (n=2816)

#### Support Devices

#### Lung Opacity

#### (n=953)

#### (n=2670)

#### Pleural Effusion

#### Cardiomegaly

#### (n=926)

#### (n=2173)

#### Lung Opacity

#### Support Devices

#### (n=918)

#### (n=1859)

#### Atelectasis

#### Atelectasis

#### (n=1313)

#### (n=842)

#### Pleural Effusion

#### UniRG-CXR MedGemma MedVersa GPT-5 GPT-4o

#### (n=1120)

#### Edema (n=663)

Enlarged Cardio.

### 0.0 0.2 0.4 0.6 0.8 1.0

#### (n=628)

#### F1

#### Pneumonia

#### (n=473)

#### (d)

#### Consolidation

#### 1.6

#### 1.6

#### (n=249)

#### Lung Lesion

#### 1.4

#### 1.4

#### (n=178)

#### No Finding

#### (n=141)

#### 1.2

#### 1.2

#### Fracture

#### (n=133)

#### 1.0

#### 1.0

#### 1/RadCliQ-v1

#### 1/RadCliQ-v1

#### Pleural Other

#### (n=106)

#### 0.8

#### 0.8

#### Pneumothorax

#### UniRG-CXR MedGemma MedVersa GPT-5 GPT-4o

#### (n=81)

#### 0.6

#### 0.6

#### Male Female Male Female

#### white non-white 0.0 0.2 0.4 0.6 0.8 1.0

#### <60 60+ Male Female Male Female

#### F1

Figure4:GeneralizationandrobustnessofUniRG-CXR.(a).Weheldouttwodatasetssources(IU-Xrayand PD(proprietarydata)fromthetrainingdataandevaluateUniRG-CXRinazero-shotsettingonthesedatasets. UniRG-CXRconsistentlyoutperformspriormodels,maintainingsubstantialperformancegainsinthischallenging setup.(b)and(c)presentcondition-levelF1scoresonMIMIC-CXRandPDandhighlightthatUniRG-CXRremains theoveralltop-performingmodelincondition-leveldiagnosticaccuracy.(d).UniRG-CXRdemonstratesstableand robustperformanceacrossgender,age,andracesubgroups,allofwhichexceedtheperformanceofthesecond-best model(thedashedlines).

Inthissection,weevaluatetherobustnessandgeneralizationofUniRG-CXR.Firstofall,arobust universalreportgenerationmodelshouldgeneralizewellacrossinstitutions,includingthosewithdata distributionsunseenduringtraining.Totestthis,wecreateanexperimentsetupwhereweintentionally leaveoutcertaindatasources(IUdataandaproprietydatasource)fromthetrainingofUniRG-CXR.We thentestthemodel’szero-shotperformanceonthesetwodatasets,asshowninFigure4(a).UniRG-CXR consistentlyachievesthebestperformanceacrossallout-of-distributiondatasets,surpassingpriorbaselines withsubstantialmargins.

Anotherkeygeneralizationofchestradiologyreportgenerationmodelsistoaccuratelyidentifyand classifyspecificthoracicdiseases/conditions,therebyexpeditingthediagnosticprocessforclinicians[14].We evaluatetheconditiondiagnosiscapabilitiesoftheoutputfromUniRG-CXRbyapplyingtheCheXbert model[20]todetectdiseasesfromitsgeneratedreports.AsshowninFigure4(b)and(c),UniRG-CXRis leadingtheperformanceacrossalltheprevalentdiseasescomparedwithotherpriormodelsinbothMIMIC andout-of-distributionproprietarydataset.

Finally, we evaluate the robustness ofUniRG-CXR across gender, age, and race.As shown in Figure 4(d), wepresentperformancestratifiedbythesedemographicsubgroupsontheCheXpert-Plusdataset.UniRG- CXRachievesconsistentlyhighscoresacrossallgroups,withoverlappingdistributionsandnonoticeable performancedropinanydemographiccategory.Moreover,allsubgroupperformancesofUniRG-CXR surpassthoseofthesecond-bestmodel(dashedline),demonstratingthatUniRG-CXRisrobustandfair acrossdemographicsubgroupswhilemaintainingsuperiorityoverpriormodels.

## Discussion

Inthiswork,weintroduceUniRG,areinforcementlearning-basedframeworkformedicalimagingreport generation.Usingthisframework,weareabletotrainUniRG-CXR,astate-of-the-artradiologyreport generationsystemforchestradiographs,whichestablishesanewperformancestandardacrossbenchmarkson theReXrankleaderboard,whichspansmultipleclinicalcontexts(inpatient,outpatient,andemergencycare) anddatafromover70medicalsites.Unlikepreviousmodels,whichoftenexcelledonisolatedbenchmarksor onspecificmetrics,UniRG-CXRdeliversconsistentperformanceimprovementacrossmultiplemetricson fourwidelyuseddatasets(MIMIC-CXR,IU-Xray,CheXpertPlus,andReXGradient)aswellasadditional proprietarydataset.

OurevaluationprotocolprovidesacomprehensiveassessmentofAI-basedradiologyreportgeneration. Webenchmarkthesystemusinglexicalsimilarity,embedding-basedsimilarity,andLLM-basedclinicalerror

metrics,enablingaholisticcomparisonagainstbothreferencereportsandcompetingmodels.Beyondthese, weconductlongitudinalevaluationsthatsimulatereal-worldradiologists’workflows,assessgeneralization androbustnessonunseendistributions,andstratifyperformancebydemographicsubgroups.Wefurther linkreport-levelqualitytocondition-leveldiagnosticaccuracy.Collectively,theseanalysesunderscorethe universality,robustness,andclinicalalignmentofUniRG-CXR

Universalacrossinstitutionsanddatadistributions Radiologyreportingpracticesvarywidelyacross institutions,regions[8],anddocumentationconventions[12].Priorsystemsoftenoverfittodataset-specific phrasingorreportingstyles,leadingtoperformancedropswhenevaluatedonunseendatasetsoracross sites[9,15,21].UniRG-CXRovercomesthislimitationbyexhibitingconsistenthighperformanceacross allbenchmarkdatasetsandonentirelyunseendistributionswithzero-shotinference,includingbothpublic andprivatecohortscollectedfromdiverseinstitutions.TheseresultsindicatethatUniRG-CXRcaptures theunderlyingclinicalsemanticsratherthanmemorizingsuperficialtextualtemplates—achievingtrue generalizationacrossdatasources,institutions,anddomains.SuchrobustnessestablishesUniRG-CXRas auniversalfoundationmodelforradiologyreporting,capableofmaintainingreliabilityandfidelityacross heterogeneousreal-worldenvironments.

Universalacrossevaluationmetrics Traditionaltext-generationmetricssuchasBLEUorROUGE correlateonlyweaklywithclinicaljudgments[13,23],oftenobscuringmedicallysignificanterrors.UniRG- CXRbridgesthisgapbyexplicitlyintegratingclinicalerrorsignalsintoitsreinforcementlearningreward design,aligningoptimizationwithradiologicalpracticeratherthansurface-levellinguisticsimilarity.As

aresult,itachievesstrongandbalancedperformanceacrossbothNLGandclinicallygroundedmetrics, representingauniversalimprovementacrossevaluationdimensions.

Universalacrossdiagnosticlevels Priorworktypicallyassessedperformanceatthereportlevel[17,26, 32],obscuringwhethermodelscapturedcriticalfindings[14].Byincorporatingdisease-levelassessments,we provideafiner-grainedviewofdiagnosticfidelity.TheseevaluationsshowcasetheabilityofUniRG-CXRto reflectdiagnosticinformation,includinginthelongtailofrareconditionswheretrainingdataaresparse.

Universalacrosslongitudinalcontexts Radiologistsoftenrelyonpriorstudieswheninterpretingnew exams [2, 3, 18, 33].While previous models primarily operated in single-study settings [32], we additionally set upthelongitudinalevaluationwherethemodelissuppliedwithnotonlycurrentCXRsbutalsopriorreports andimages.UniRG-CXRexcelsinbothstandardandlongitudinalconditions.Iteffectivelyintegratesprior imagesandreportstoproduceclinicallycoherentupdates,achievingstate-of-the-artresultsintemporal reasoninganddemonstratingsuperiorlongitudinalmodelingcapability.

Universalacrossdemographics WefurthervalidateUniRG-CXRacrossstratifieddemographicsubgroups,confirmingrobustandequitableperformanceacrossgender,age,andrace.Thisfairnessevaluation iscriticalforreal-worlddeployment,ensuringminimalbiasandconsistentreportqualityacrosspatient populations.

Overall,UniRG-CXRrepresentsasubstantialadvanceinradiologyreportgeneration,unifyinghigh performanceacrossdatasets,metrics,diagnosticlevels,longitudinalsetups,anddemographicsubgroups. Beyondsurpassingpriorsystems,itembodiestheprinciplesofuniversality,generalizability,andclinical alignment,pavingthewayforreliablereal-worlddeployment.Inthelongerterm,augmentingthissystem withinteractive,instruction-followingcapabilitiesandexpandingtomultimodalpatientdata(e.g.,labtests, priorimaging,andclinicalnotes)couldfurtherenhanceitsclinicalutility.WeanticipatethatUniRG-CXR willserveasbothastrongbenchmarkforfutureresearchandafoundationforbuildingreliable,assistiveAI systemsinradiology.

## Methods

#### Model

UniRG-CXRisbuiltbyfine-tuningastate-of-the-artopen-sourcevision–languagefoundationmodel,Qwen3- VL-8B-Instruct [1] for the report generation tasks.In the sections that follow, we describe our task formulation, inferenceandevaluationprotocols,optimizationstrategy,anddatasetcurationindetail.

#### Tasks

Ourmodelistrainedtogenerateboththe‘findings’and‘impression’sectionsofthereportforafrontalview (anterior–posterior or posterior–anterior) of the chest radiograph,which typically capture the key observations

madeinastudy.Themodelreceivesadditionalcontextualinformation,includingthestudyindicationand anyavailablecomparisontext.Toimprovecomputationalefficiency,eachradiographisresizedtoaresolution of512×512pixels.Inroutineclinicalpractice,radiologistsfrequentlyreferencepriorimagesandprior reportswheninterpretingthecurrentstudy.Tomirrorthisworkflowandenhanceclinicalfidelity,wealso supplythemodelwiththemostrecentpriorfrontalradiographanditsassociatedreportassupplementary inputs.

#### InferenceandEvaluationMetrics

#### WefollowtheexactsetupfromReXranktotakeintoaccountcontext(indication+comparison).Weonly

usethekeyimagepathprovidedbyReXrankwhichistypicallyfrontalviewimage.Wekeeptemperatureas 0forinference.WefollowthesetupsinReXrank[29]toevaluatereportqualityusingthefollowingmetrics:

BLEU-2[16].BLEUisastandardmetricformachinetranslationandtextgenerationthatmeasures n-gramprecisionbetweengeneratedandreferencetexts(0–1scale).FollowingZhangetal.[29],wereport BLEU-2,whichcapturesbigramprecision.

BERTScore[7,28].BERTScoreevaluatessemanticsimilaritybycomputingcosinesimilaritybetween BERTembeddingsofthegeneratedandreferencereports,providingameaning-awarealternativetosurface n-grammetrics.

SembScore[20].SembScoreisaradiology-specificmetricthatcomputescosinesimilaritybetween14pathologyindicatorvectorsproducedbytheCheXbertlabelerforgeneratedandgroundtruthreports.

RadGraph-F1[10]measurestheoverlapinclinicalentitiesandrelationsextractedbyRadGraphfrom candidateandreferencereports.

1/RadCliQ-v1 [24] is the reciprocal of the RadCliQ composite metric, which aggregates BLEU, BERTScore, SembScore,andRadGraph-F1forholisticradiologyreportevaluation.BecauseRadCliQisoriginallyloweris-better,wefollowReXrank[29]andreportitsinversesothathighervaluesindicatebetterperformanceto beconsistentwithotherscores.

RaTEScore[31]isanentity-centricmetricemphasizingkeymedicalconceptssuchasdiagnosesand anatomicalstructures,whilebeingrobusttomedicalsynonymsandnegation.

CheXprompt[26]InadditiontotheReXrankleaderboardmetrics,wealsoevaluatereportqualitywith CheXprompt,anLLM-basederrordetectionmetric.

#### Optimization

UniRG-CXRfollowsatwo-stageSFT+RLtrainingpipelineaswefoundthatthecombinedapproachis betterthanSFTaloneorRLalone(detailsareinthesupplementaryinformationsection).

IntheSFTstage,themodelisinitializedwithastrongfoundationforradiologyreportgeneration. TheSFTtrainingisperformedoverfourdatasets:MIMIC,CheXpert-Plus,ReXGradientandIUandwe conductagridsearchoverlearningrates[1 × 10−5,5 × 10−5]andbatchsizes[128,256,521].Theoptimal configurationisalearningrateof5 × 10−5withabatchsizeof256for3epochs.

In the RLstage,we adopt GRPO [19] as our reinforcement learning algorithm,which eliminates the need forvaluefunctionsbycomputingadvantageswithinquery-specificgroups.Followingrecentadvances[25], weincorporatetwokeyimprovements:(1)ahigherclippingthresholdtoencourageresponsediversityand prevententropycollapse;(2)removeKLpenalty.Ourtrainingadoptsalearningrateof5 × 10−6,aglobal batchsizeof256,and16sampledrolloutsperquery.TheRLtrainingisperformedoverfourdatasets: MIMIC,CheXpert-Plus,ReXGradientandIU.ForrewardoptimizationintheRLstage,wetargetBLEU, BERTScore,RadGraph-F1,SembScore,andCheXprompt(LLM-based),withoutusinganyformatrewards sincethemodelreliablyproduceswell-structuredreportsafterSFT.OurRLprocedurefollowsatwo-step optimizationstrategy.

Step1:RadCliQ-orientedoptimization.Wefirstoptimizeaweightedcompositerewardconsistingof BLEU,BERTScore,SembScore,andRadGraph-F1,usingtheRadCliQcoefficients[24]of0,0.370,0.253,and 0.377,respectively.This stage runsfor one epoch and encourages themodel to generateoutputs that are both lexicallyandclinicallyalignedwiththeground-truthreports,effectivelytargetingRadCliQimprovement.

Step2:Error-reductionoptimization.StartingfromthebestcheckpointfromStep1’sRadCliQ optimization,weperformanadditionalepochinwhichweincorporatetheCheXprompterrormetricinto thereward.Specifically,weuse1/(#CheXprompterrors + 1)astheCheXpromptrewardtoincentivize reducingfactualreportingerrors.TopreservetheRadCliQperformanceachievedinStep1,weintegratethe CheXpromptrewardwithaweightof0.5alongsidethepreviousmetrics.WealsoapplyaKLregularization termwithcoefficient0.03topreventexcessivedeviationfromtheStep1policy.

#### DatasetDetails

OurtrainingdataconsistsofthetrainingsplitsfromMIMIC-CXR,CheXpertPlus,ReXGradientandIU. Weextractedtheindication,comparison,findings,andimpressionsectionsfromthecorrespondingradiology

reports.Wethenremovedstudiesinwhichboththefindingsandimpressionsectionswereempty.Studies thatcontainedafindingssectionbutlackedanimpression,orcontainedanimpressionbutlackedfindings, wereretained.Dependingonwhichground-truthsectionswereavailable(findingsand/orimpression),we

applieddifferentprompttemplates,asshowninthesupplementaryinformationsection.Wealsosetaside 1,024samplesfromtheMIMIC-CXRtrainingsetasavalidationsetforallexperiments. WefollowReXrankevaluationtoevaluateUniRG-CXRonReXrankofficialtestsetsfromMIMIC-CXR, CheXpert Plus, IU-Xray and ReXGradient private test set.Apart from the ReXrank testsets, we also evaluate onaproprietarydatasetwhichwenameasPD.Belowarethedetailsforeachdataset.

MIMIC-CXR [11].Alarge,publiclyavailabledatasetcontaining377,110chestX-raysfrom227,835 studiescollectedattheBethIsraelDeaconessMedicalCenterinBoston,MA.Allimagesandreportsare fullyde-identified.WeusetheofficialReXrankMIMICtestset,whichincludes2,347studies,forevaluation, andusetheremainingtrainingsplitformodeldevelopment.

CheXpertPlus [4]Apubliclyavailabledatasetcomprising223,462pairedradiologyreportsandchest x-raysfrom187,711studiesacross64,725patients.WeadopttheReXranktestset,whichfollowstheofficial CheXpertPlustestsplitandcontains200studies.TheCheXpertPlustrainingsplitisusedfortraining UniRG-CXR.

ReXGradient [30]Alarge-scaledatasetcuratedbyGradientHealth,consistingofaprivatetestsetof 10,000studiesfrom7,004patientsacross67clinicalsitesintheUnitedStates.Thepubliclyreleasedofficial trainingset,comprising140,000studies,isusedfortrainingUniRG-CXR.

IU-Xray [6]Apublicdatasetcontaining7,470radiologyreportspairedwithcorrespondingfrontaland lateralchestx-rays.WefollowtheReXranksplitandevaluateonthetestsetof590studiesandtrainwith therestasthetrainset.Toassessthezero-shotgeneralizationcapabilityofUniRG-CXRonunseendata sources,weexcludetheIU-Xraytrainingsetfromthetrainingcorpusinthegeneralizationstudy.

ProprietaryDataset(PD) Thisproprietarydatasetcomprises11,815chestX-raystudiesfrominpatient andoutpatientfacilitiesacrosstheUnitedStates.Eachstudyincludescorrespondingradiologyreportsof frontalandlateralviewimages,withoutpriorstudies.Thedatasetwasusedexclusivelyforevaluation,with nooverlapwithanytrainingsources.

## References

#### [1]ShuaiBai,YuxuanCai,RuizheChen,KeqinChen,XionghuiChen,ZesenCheng,LianghaoDeng,Wei

Ding,ChangGao,ChunjiangGe,WenbinGe,ZhifangGuo,QidongHuang,JieHuang,FeiHuang, BinyuanHui,ShutongJiang,ZhaohaiLi,MingshengLi,MeiLi,KaixinLi,ZichengLin,JunyangLin, XuejingLiu,JiaweiLiu,ChenglongLiu,YangLiu,DayihengLiu,ShixuanLiu,DunjieLu,RuilinLuo, ChenxuLv,RuiMen,LingchenMeng,XuanchengRen,XingzhangRen,SiboSong,YuchongSun,Jun Tang,JianhongTu,JianqiangWan,PengWang,PengfeiWang,QiuyueWang,YuxuanWang,Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu, Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen Yu, Fei Zhang,HangZhang,XiZhang,BoZheng,HumenZhong,JingrenZhou,FanZhou,JingZhou,Yuanzhi Zhu,andKeZhu.Qwen3-vltechnicalreport,2025.URLhttps://arxiv.org/abs/2511.21631.

#### [2]ShruthiBannur,StephanieHyland,QianchuLiu,FernandoPerez-Garcia,MaximilianIlse,DanielC

Castro,BenediktBoecking,HarshitaSharma,KenzaBouzid,AnjaThieme,etal.Learningtoexploit temporal structure for biomedical vision-language processing. In Proceedings of the IEEE/CVF Conference onComputerVisionandPatternRecognition,pp.15016–15027,2023.

#### [3]ShruthiBannur,KenzaBouzid,DanielC.Castro,AntonSchwaighofer,AnjaThieme,SamBond-Taylor,

MaximilianIlse,FernandoP´erez-Garc´ıa,ValentinaSalvatelli,HarshitaSharma,FelixMeissen,Mercy Ranjit,ShaurySrivastav,JuliaGong,NoelC.F.Codella,FabianFalck,OzanOktay,MatthewP. Lungren,MariaTeodoraWetscherek,JavierAlvarez-Valle,andStephanieL.Hyland.Maira-2:Grounded radiologyreportgeneration,2024.URLhttps://arxiv.org/abs/2406.04449.

#### [4]PierreChambon,Jean-BenoitDelbrouck,ThomasSounack,Shih-ChengHuang,ZhihongChen,Maya

Varma,StevenQHTruong,ChuTheChuong,andCurtisP.Langlotz.Chexpertplus:Augmentinga largechestx-raydatasetwithtextradiologyreports,patientdemographicsandadditionalimageformats, 2024.URLhttps://arxiv.org/abs/2405.19538.

#### [5]Jean-BenoitDelbrouck,JustinXu,JohannesMoll,AloisThomas,ZhihongChen,SophieOstmeier,

AsfandyarAzhar,KelvinZhenghaoLi,AndrewJohnston,ChristianBluethgen,etal.Automated structuredradiologyreportgeneration.InProceedingsofthe63rdAnnualMeetingoftheAssociationfor ComputationalLinguistics(Volume1:LongPapers),pp.26813–26829,2025.

#### [6]Dina Demner-Fushman, Marc D Kohli, Marc B Rosenman, Sonya E Shooshan, Laritza Rodriguez, Sameer

Antani,GeorgeRThoma,andClementJMcDonald.Preparingacollectionofradiologyexaminations fordistributionandretrieval,2015.

#### [7]JacobDevlin,Ming-WeiChang,KentonLee,andKristinaToutanova.Bert:Pre-trainingofdeep

bidirectionaltransformersforlanguageunderstanding.InProceedingsofthe2019conferenceofthe NorthAmericanchapteroftheassociationforcomputationallinguistics:humanlanguagetechnologies, volume1(longandshortpapers),pp.4171–4186,2019.

#### [8]MichaelPHartung,IanCBickle,FrankGaillard,andJeffreyPKanne.Howtocreateagreatradiology

report.Radiographics,40(6):1658–1670,2020.

#### [9]JonathanHuang,LukeNeill,MatthewWittbrodt,DavidMelnick,MatthewKlug,MichaelThompson,

John Bailitz,Timothy Loftus,Sanjeev Malik,Amit Phull,et al.Generative artificial intelligence for chest radiographinterpretationintheemergencydepartment.JAMAnetworkopen,6(10):e2336100–e2336100, 2023.

#### [10]SaahilJain,AshwinAgrawal,AdrielSaporta,StevenTruong,DuNguyenDuong,TanBui,Pierre

Chambon,YuhaoZhang,MatthewPLungren,AndrewYNg,etal.Radgraph:Extractingclinical entities and relations from radiology reports.In Thirty-fifthConferenceonNeuralInformationProcessing SystemsDatasetsandBenchmarksTrack(Round1),2021.

#### [11]AlistairEWJohnson,TomJPollard,SethJBerkowitz,NathanielRGreenbaum,MatthewPLungren,

Chih-ying Deng, Roger G Mark, and Steven Horng.Mimic-cxr, a de-identified publicly available database ofchestradiographswithfree-textreports.Scientificdata,6(1):317,2019.

#### [12]Charles E Kahn Jr, Curtis P Langlotz, Elizabeth S Burnside, John A Carrino, David S Channin, David M

Hovsepian,andDanielLRubin.Towardbestpracticesinradiologyreporting.Radiology,252(3):852–856, 2009.

#### [13]GuanxiongLiu,Tzu-MingHarryHsu,MatthewMcDermott,WillieBoag,Wei-HungWeng,Peter

Szolovits, and Marzyeh Ghassemi.Clinically accurate chest x-ray report generation.In MachineLearning forHealthcareConference,pp.249–269.PMLR,2019.

#### [14]MEMilamandCWKoo.Thecurrentstatusandfutureoffda-approvedartificialintelligencetoolsin

chestradiologyintheunitedstates.ClinicalRadiology,78(2):115–122,2023.

#### [15]AaronNicolson,JasonDowling,andBevanKoopman.ImprovingchestX-rayreportgenerationby

leveragingwarmstarting. ArtificialIntelligenceinMedicine,144:102633,2023. ISSN0933-3657. doi:https://doi.org/10.1016/j.artmed.2023.102633.URLhttps://www.sciencedirect.com/science/article/pii/S0933365723001471.

#### [16]Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu.Bleu:a method for automatic evaluation

ofmachinetranslation.InProceedingsofthe40thannualmeetingoftheAssociationforComputational Linguistics,pp.311–318,2002.

#### [17]AndrewSellergren,SaharKazemzadeh,TiamJaroensri,AtillaKiraly,MadeleineTraverse,Timo

Kohlberger,ShawnXu,FayazJamil,C´ıanHughes,CharlesLau,JustinChen,FereshtehMahvar,Liron Yatziv,TiffanyChen,BramSterling,StefanieAnnaBaby,SusannaMariaBaby,JeremyLai,Samuel

Schmidgall,LuYang,KejiaChen,PerBjornsson,ShashirReddy,RyanBrush,KennethPhilbrick,Mercy Asiedu,InesMezerreg,HowardHu,HowardYang,RichaTiwari,SunnyJansen,PreetiSingh,YunLiu, ShekoofehAzizi,AishwaryaKamath,JohanFerret,ShreyaPathak,NinoVieillard,RamonaMerhej, SarahPerrin,TatianaMatejovicova,AlexandreRam´e,MorganeRiviere,LouisRouillard,Thomas Mesnard,GeoffreyCideron,JeanbastienGrill,SabelaRamos,EdouardYvinec,MichelleCasbon, ElenaBuchatskaya,Jean-BaptisteAlayrac,DmitryLepikhin,VladFeinberg,SebastianBorgeaud,Alek Andreev,CassidyHardin,RobertDadashi,L´eonardHussenot,ArmandJoulin,OlivierBachem,Yossi Matias,KatherineChou,AvinatanHassidim,KaviGoel,ClementFarabet,JoelleBarral,TrisWarkentin, JonathonShlens,DavidFleet,VictorCotruta,OmarSanseviero,GusMartins,PhoebeKirk,Anand Rao,ShravyaShetty,DavidF.Steiner,CanKirmizibayrak,RoryPilgrim,DanielGolden,andLinYang. Medgemmatechnicalreport,2025.URLhttps://arxiv.org/abs/2507.05201.

#### [18]Francesco Dalla Serra, Chaoyang Wang, Fani Deligianni, Jeffrey Dalton, and Alison Q O’Neil. Controllable

chestx-rayreportgenerationfromlongitudinalrepresentations.arXivpreprintarXiv:2310.05881,2023.

#### [19]ZhihongShao,PeiyiWang,QihaoZhu,RunxinXu,JunxiaoSong,XiaoBi,HaoweiZhang,Mingchuan

Zhang,YKLi,etal.Deepseekmath:Pushingthelimitsofmathematicalreasoninginopenlanguage models.arXivpreprintarXiv:2402.03300,2024.

[20]AkshaySmit,SaahilJain,PranavRajpurkar,AnujPareek,AndrewY.Ng,andMatthewP.Lungren.

Chexbert:Combiningautomaticlabelersandexpertannotationsforaccurateradiologyreportlabeling usingbert,2020.URLhttps://arxiv.org/abs/2004.09167.

#### [21]TimTanida,PhilipM¨uller,GeorgiosKaissis,andDanielRueckert.Interactiveandexplainableregion

guidedradiologyreportgeneration.InCVPR,2023.

#### [22]AliceCYu,BahramMohajer,andJohnEng.Externalvalidationofdeeplearningalgorithmsfor

radiologicdiagnosis:asystematicreview.Radiology:ArtificialIntelligence,4(3):e210064,2022.

#### [23]FeiyangYu,MarkEndo,RayanKrishnan,IanPan,AndyTsai,EduardoPontesReis,EduardoKaiser

UrurahyNunesFonseca,HenriqueMinHoLee,ZahraShakeriHosseinAbad,AndrewYNg,etal. Evaluatingprogressinautomaticchestx-rayradiologyreportgeneration.Patterns,4(9),2023.

#### [24]FeiyangYu,MarkEndo,RayanKrishnan,IanPan,AndyTsai,EduardoPontesReis,EduardoKaiser

UrurahyNunesFonseca,HenriqueMinHoLee,ZahraShakeriHosseinAbad,AndrewYNg,etal. Evaluatingprogressinautomaticchestx-rayradiologyreportgeneration.Patterns,4(9),2023.

#### [25]QiyingYu,ZhengZhang,RuofeiZhu,YufengYuan,XiaochenZuo,YuYue,WeinanDai,TiantianFan,

GaohongLiu,LingjunLiu,etal.Dapo:Anopen-sourcellmreinforcementlearningsystematscale. arXivpreprintarXiv:2503.14476,2025.

#### [26]JuanManuelZambranoChaves,Shih-ChengHuang,YanboXu,HanwenXu,NaotoUsuyama,Sheng

Zhang, Fei Wang, Yujia Xie, Mahmoud Khademi, Ziyi Yang, et al.A clinically accessible small multimodal radiologymodelandevaluationmetricforchestx-rayfindings.NatureCommunications,16(1):3108, 2025.

#### [27]JuanManuelZambranoChaves,Shih-ChengHuang,YanboXu,HanwenXu,NaotoUsuyama,Sheng

Zhang, Fei Wang, Yujia Xie, Mahmoud Khademi, Ziyi Yang, et al.A clinically accessible small multimodal radiologymodelandevaluationmetricforchestx-rayfindings.NatureCommunications,16(1):3108, 2025.

#### [28]TianyiZhang,VarshaKishore,FelixWu,KilianQWeinberger,andYoavArtzi.Bertscore:Evaluating

textgenerationwithbert.InInternationalConferenceonLearningRepresentations,2019.

#### [29]XiaomanZhang,Hong-YuZhou,XiaoliYang,OishiBanerjee,Juli´anNAcosta,JoshMiller,Ouwen

Huang, and Pranav Rajpurkar.Rexrank:A public leaderboard for ai-powered radiology report generation. arXivpreprintarXiv:2411.15122,2024.

#### [30]XiaomanZhang,Juli´anN.Acosta,JoshMiller,OuwenHuang,andPranavRajpurkar.Rexgradient

160k:Alarge-scalepubliclyavailabledatasetofchestradiographswithfree-textreports,2025.URL https://arxiv.org/abs/2505.00228.

#### [31]WeikeZhao,ChaoyiWu,XiaomanZhang,YaZhang,YanfengWang,andWeidiXie.Ratescore:A

metricforradiologyreportgeneration.InProceedingsofthe2024ConferenceonEmpiricalMethodsin NaturalLanguageProcessing,pp.15004–15019,2024.

#### [32]Hong-YuZhou,Juli´anNicol´asAcosta,SubathraAdithan,SuvrankarDatta,EricJ.Topol,andPranav

Rajpurkar.Medversa:Ageneralistfoundationmodelformedicalimageinterpretation,2025.URL https://arxiv.org/abs/2405.07988.

#### [33]QingqingZhu,TejasSudharshanMathai,PritamMukherjee,YifanPeng,RonaldMSummers,and

ZhiyongLu.Utilizinglongitudinalchestx-raysandreportstopre-fillradiologyreports.InInternational ConferenceonMedicalImageComputingandComputer-AssistedIntervention,pp.189–198.Springer,

2023.

### SupplementaryInformation

#### ComparingSFTandRL

Toidentifythemosteffectivetrainingstrategyforradiologyreportgeneration,wecomparethreeapproaches ontheMIMICdataset:SFTalone,RLalone,andthecombinedSFT+RLpipeline.AllSFTandRLruns aretrainedfor3epochs,whiletheSFT+RLconfigurationappliesanadditional2epochsofRLstarting fromtheSFTcheckpoint.AsshowninTable1,RLaloneoutperformsSFTonBERTScoreandSembScore, butlagssignificantlybehindonRadGraph-F1.ThisislikelybecauseRadGraphismoresensitivetospecific wording,phrasing,andlexicaldistributions,whichSFTcapturesmoredirectlythroughnext-tokenprediction. Consequently,SFTslightlyoutperformsRLontheoverallRadCliQscore.ThecombinedSFT+RLsetup yieldsthestrongestresultsacrossallmetrics.SFTfirstteachesthemodeltheoutputformatanddatasetspecificlexicalstructure,andRLsubsequentlyrefinesthisfoundationbyoptimizingmoresemanticallyand clinicallyalignedrewards,leadingtothebestsynergyandoverallperformance.

Table1:ComparisonofSFT,RL,andSFT+RLonfindings+impressiongenerationonMIMIC.Thecombined SFT+RLstrategyachievesthebestperformance.

#### Method BERTScore SembScore RadGraph-F1 1/RadCliQ

Baseline 0.293 0.242 0.102 0.625 MIMICSFT 0.421 0.426 0.236 0.962 MIMICRL 0.437 0.435 0.198 0.950 MIMICSFT+MIMICRL 0.449 0.478 0.267 1.110

#### PromptTemplates

Below are training and inference prompt templates for findings + impression generation and findings generation. {input}istheplaceholderfortheinputimagesandthecontextfromtheindicationandcomparisonsections.

#### Findings+ImpressionGenerationPrompt

Thisisaradiologyreportgenerationtask.Hereisthecontext:{input}Giventheimageandthe context,providethereportinthefollowingformat:Findings:[writethefindings]Impression:[write theimpression]Nowwritethereportintheformatabove.

#### FindingsGenerationPrompt

Thisisaradiologyreportgenerationtask.Hereisthecontext:{input}Giventheimageandthe context,providethefindingsinthefollowingformat:Findings:[writethefindings]Nowwritethe reportintheformatabove.
