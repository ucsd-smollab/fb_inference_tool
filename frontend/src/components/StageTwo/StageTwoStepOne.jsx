import { Link } from "react-router-dom";

import styles from "./StageTwoStepOne.module.css";
import globalStyles from "./StageTwo.module.css"

const StageTwoStepOne = (props) => {

  const sections = ["information you share", "content you post", "your web browsing", "content your friends post", "your activity on facebook", "...and more"]

  return (
    <div className={globalStyles.background}>
      <br />
      <div className={styles.MainBodyContainer}>
        <div style={{"marginTop": "150px"}}>
          <span className={styles.CenterTitle}>Facebook can learn about you from:</span>
        </div>
        <div className={styles.ContentContainer}>
          {sections.map((section) => 
            <div className={styles.SectionContainer}>
              <span className={styles.SectionHeader}>{section}</span>
              <div className={styles.SectionImage}></div>
              <div style={{width:"300px", height:"300px", backgroundColor:"black"}}></div>
              <br />
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
