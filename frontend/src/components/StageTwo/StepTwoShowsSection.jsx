import styles from "./StageTwoStepTwo.module.css";

const StepTwoShowsSection = (props) => {
  return (
    <div className={styles.SectionContainer}>
      <span>Facebook Shows</span>
      <div className={styles.AdImage}></div>
      <div className={styles.AdImage}></div>
    </div>
  );
};

export default StepTwoShowsSection;
