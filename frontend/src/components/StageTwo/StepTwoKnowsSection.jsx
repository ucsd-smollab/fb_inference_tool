import globalStyles from "../../styles/styles.module.css";
import styles from "./StageTwoStepTwo.module.css";

const StepTwoKnowsSection = (props) => {
  const row = [
    ["lives in San Diego", "shared directly"],
    ["lived in Los Angeles", "shared directly"],
    ["interested in nature photography", "inferred from posts"],
    ["visited Yosemite", "inferred from friend's post"],
    ["stayed at Madison Campground", "inferred from posts invisible"],
    ["interested in Classical Music", "inferred from web browsing"],
    ["interested in cooking", "inferred from activity"]
  ];



  return (
    <div className={`${globalStyles.flex_container} ${globalStyles.three_column}`}>
      <h1>Facebook Knows</h1>
      <div className={styles.body_container}>
        {row.map((item, index) => {
          return (
              <div className={styles.left_and_right}>
                <span className={styles.left}>{item[0]}</span> 
                <span className={styles.right}>{item[1]}</span>
                <br/>
              </div>
          );
        })}
      </div>
    </div>
  );
};

export default StepTwoKnowsSection;
