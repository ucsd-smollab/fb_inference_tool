import { Link } from "react-router-dom";

import styles from "./StageTwoStepOne.module.css";
import globalStyles from "./StageTwo.module.css"

const StageTwoStepOne = (props) => {

  const sections = ["information you share", "content you post", "your web browsing", "content your friends post", "your activity on facebook", "...and more"]

  return (
    <div style={{backgroundColor: "lightGray"}}>
      <div className={globalStyles.StageTitleContainer}>
        <span className={globalStyles.StageTitle}>Stage 2.1</span>
      </div>
      <br />
      <div className={styles.MainBodyContainer}>
        <span className={styles.CenterTitle}>Facebook can learn about you from:</span>
        <div className={styles.ContentContainer}>
          {sections.map((section) => 
            <div className={styles.SectionContainer}>
              <span>{section}</span>
              <div style={{backgroundColor: "black", width: "200px", height: "200px"}}></div>
            </div>
          )}
        </div>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageTwoStepTwo">
          <button className={globalStyles.ButtonNav}>
            Next
          </button>
        </Link>
      </div>
    </div>
  );
}

export default StageTwoStepOne;
