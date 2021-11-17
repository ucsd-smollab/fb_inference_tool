import globalStyles from "../../styles/styles.module.css";
import styles from "./StageTwoStepTwo.module.css";

import masterclass from "../../images/ad-masterclass.png";
import secret from "../../images/ad-secret.png";

const StepTwoShowsSection = (props) => {
  return (
    <div className={`${globalStyles.flex_container} ${globalStyles.three_column}`}>
      <h1>Facebook Shows</h1>
      <img className={styles.ad_masterclass} src={masterclass}></img>
      <img className={styles.ad_secret} src={secret}></img>
    </div>
  );
};

export default StepTwoShowsSection;
