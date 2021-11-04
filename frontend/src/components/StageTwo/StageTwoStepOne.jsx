import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageTwoStepOne.module.css";

import like from "../../images/blue-like.png";
import search_like from "../../images/search-and-like.png";
import claire_mairy from "../../images/claire-with-mary.png";
import browse from "../../images/search-history.png";
import content from "../../images/mary-at-zion.png";

const StageTwoStepOne = (props) => {

  const sections = ["information you share", "content you post", "your web browsing", "content your friends post", "your activity on facebook", "...and more"]

  return (
    <div>
      <h1>Facebook can learn about you from:</h1>
      <div style={{display: 'flex', justifyContent: 'center'}} >
        <ul class={styles.flex_container}>
          <li class={styles.flex_item}>
            information you share
            <br/>
            <img class={styles.image_content} src={content}/>
            </li>
          <li class={styles.flex_item}>
            content you post
            <br/>
            <img class={styles.image_content} src={content}/>
            </li>
          <li class={styles.flex_item}>
            your web browsing
            <br/>
            <img class={styles.image_browse} src={browse}/>
            </li>
          <li class={styles.flex_item}>
            content your friends post
            <br/>
            <img class={styles.image_content} src={claire_mairy}/>
            </li>
          <li class={styles.flex_item}>
            your activity on Facebook
            <br/>
            <img class={styles.image_activity} src={search_like}/>
          </li>
          <li class={styles.flex_item}>
            ...and more
            <br/>
            <img class={styles.image_more} src={like}/>
          </li>
        </ul>
        <div className={globalStyles.ButtonContainer}>
          <Link to="/StageTwoStepTwo">
            <button className={globalStyles.ButtonNav}>
              Next
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default StageTwoStepOne;
