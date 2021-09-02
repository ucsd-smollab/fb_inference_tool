import styles from "./StageTwoStepTwo.module.css";

const StepTwoKnowsSection = (props) => {
  const details = [
    "lives in San Diego",
    "lived in Los Angeles",
    "is interested in nature photography",
    "visited Yellowstone",
    "stayed at Madison Campground",
    "is interested in Classical Music",
    "is interested in cooking",
  ];

  const facebookDetails = [
    "shared directly",
    "shared directly",
    "inferred from posts",
    "inferred from friend's post",
    "inferred from posts invisible",
    "inferred from web browsing",
    "inferred from activity",
  ];

  return (
    <div className={styles.SectionContainer}>
      <span className={styles.SectionHeader}>Facebook Knows Abby</span>
      <div className={styles.InferencesContainer}>
        <div className={styles.DetailColumnContainer}>
          {details.map((detail) => 
            <div className={styles.DetailItemLeft}>
              <span>{detail}</span>
            </div>
          )}
        </div>
        <div className={styles.DetailColumnContainer}>
          {facebookDetails.map((detail) => 
            <div className={styles.DetailItemRight} style={{textAlign: "left"}}>
              <span className={styles.SubDetailText}>{detail}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StepTwoKnowsSection;
