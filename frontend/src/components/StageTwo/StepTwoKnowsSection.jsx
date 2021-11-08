import styles from "./StageTwoStepTwo.module.css";

const StepTwoKnowsSection = (props) => {
  const row = [
    ["lives in San Diego",
    "lived in Los Angeles",
    "is interested in nature photography",
    "visited Yellowstone",
    "stayed at Madison Campground",
    "is interested in Classical Music",
    "is interested in cooking",],
  ["shared directly",
    "shared directly",
    "inferred from posts",
    "inferred from friend's post",
    "inferred from posts invisible",
    "inferred from web browsing",
    "inferred from activity",]];

  return (
    <div className={styles.SectionContainer}>
      <span className={styles.SectionHeader}>Facebook Knows</span>
      <div className={styles.InferencesContainer}>
        <div className={styles.knowsColumn}>
          {row.map((leftItem, rightItem) => 
            <div className={styles.rowItem}>
              <span className={styles.DetailItemLeft}>{leftItem}</span>
              <span className={styles.DetailItemRight}>{rightItem}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StepTwoKnowsSection;
