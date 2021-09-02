import styles from "./StageTwoStepTwo.module.css";

const StepTwoShowsSection = (props) => {
  return (
    <div className={styles.SectionContainer}>
      <span className={styles.SectionHeader}>Facebook Shows</span>
      <img className={styles.AdImage} src="./Facebook-AD1.png" alt="facebook ad"></img>
      <img className={styles.AdImage} src="./Facebook-AD1.png" alt="facebook ad"></img>
    </div>
  );
};

export default StepTwoShowsSection;
