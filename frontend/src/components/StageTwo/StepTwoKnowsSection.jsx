import styles from "./StageTwoStepTwo.module.css";

const StepTwoKnowsSection = (props) => {
  const details = [
    "lives in San Diego",
    "lived in Los Angeles",
    "interest in nature photography",
    "visited Yellowstone",
    "stayed at Madison Campground",
    "interest in Classical Music",
    "interested in cooking",
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
      <span>Facebook Knows</span>
      <div className={styles.InferencesContainer}>
        <div className={styles.DetailColumnContainer}>
          {details.map((detail) => 
            <div className={styles.DetailItem}>
              <span>{detail}</span>
            </div>
          )}
        </div>
        <div className={styles.DetailColumnContainer}>
          {facebookDetails.map((detail) => 
            <div className={styles.DetailItem}>
              <span className={styles.SubDetailText}>{detail}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StepTwoKnowsSection;
