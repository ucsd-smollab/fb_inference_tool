import styles from "./StageTwoStepTwo.module.css";

const StepTwoProfileSection = (props) => {
  return (
    <div className={styles.SectionContainer}>
      <span>Abby Posts</span>
      <br />
      <div className={styles.ProfileImage}></div>
      <span>Abby</span>
      <br />
      <span>Lives in San Diego, California</span>
      <span>From Los Angeles, California</span>
      <br />
      <div className={styles.ProfilePostsContainer}>
        <span>
          I got to try out my new camera at Yellowstone this past weekend.
        </span>
        <div className={styles.ProfilePostImage}></div>
      </div>
      <br />
      <div className={styles.ProfilePostsContainer}>
        <span>Claire is with Mary at Madison Campground</span>
        <div className={styles.ProfilePostImage}></div>
      </div>
    </div>
  );
};

export default StepTwoProfileSection;
