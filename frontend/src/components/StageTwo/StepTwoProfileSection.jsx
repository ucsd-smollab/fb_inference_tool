import styles from "./StageTwoStepTwo.module.css";
import abby from "../../images/abby.png";

const StepTwoProfileSection = (props) => {
  return (
    <div className={styles.SectionContainer}>
      <span className={styles.SectionHeader}>Abby Posts</span>
      <div className={styles.ItemContainer}>
        <img src={abby} className={styles.ProfileImage} alt="Abby's profile picture"/>
        <span className={styles.ProfileText}>Abby</span>
      </div>

      <div className={styles.ItemContainer}>
        <span className={styles.ProfileText}>
          Lives in San Diego, California
        </span>
        <span className={styles.ProfileText}>From Los Angeles, California</span>
      </div>

      <div className={styles.ItemContainer}>
        <span className={styles.ProfileText}>
          I got to try out my new camera at Yellowstone this past weekend.
        </span>
        <br />
        <div className={styles.ProfilePostImage}></div>
      </div>

      <div className={styles.ItemContainer}>
        <span className={styles.ProfileText}>
          Claire is with Mary at Madison Campground
        </span>
        <br />
        <div className={styles.ProfilePostImage}></div>
      </div>
    </div>
  );
};

export default StepTwoProfileSection;
