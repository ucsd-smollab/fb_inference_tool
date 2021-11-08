import styles from "./StageTwoStepTwo.module.css";
import abby from "../../images/abby.png";
import lived from "../../images/lived.png";
import yosemite from "../../images/Yosemite.png";
import madison from "../../images/Madison.png";


const StepTwoProfileSection = (props) => {
  return (
    <div className={styles.flex_container}>
      <h1>Abby Posts</h1>
      <img className={styles.image_abby} src={abby}></img>
      <div className={styles.body}>Abby</div>
      <br/>
      <div>
        <img className={styles.image_lived} src={lived}></img>
        <img className={styles.image_yosemite} src={yosemite}></img>
        <img className={styles.image_madison} src={madison}></img>
      </div>
    </div>
  );
};

export default StepTwoProfileSection;
