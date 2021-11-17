import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageTwoStepOne.module.css";

import like from "../../images/blue-like.png";
import share from "../../images/share.png";
import post from "../../images/post.png";
import browse from "../../images/browse.png";
import friend_post from "../../images/friend-post.png";
import activity from "../../images/activity.png";

const StageTwoStepOne = (props) => {
  return (
    <div className={globalStyles.background}>
      <h1>Facebook can learn about you from:</h1>
      <div class={globalStyles.mainContent} >
        <ul class={`${globalStyles.flex_container} ${globalStyles.two_column}`}>
          <li class={globalStyles.itemBoxes}>
            information you share
            <br/>
            <img class={styles.image_lives} src={share}/>
            </li>
          <li class={globalStyles.itemBoxes}>
            content you post
            <br/>
            <img class={styles.image_content} src={post}/>
            </li>
          <li class={globalStyles.itemBoxes}>
            your web browsing
            <br/>
            <img class={styles.image_browse} src={browse}/>
            </li>
          <li class={globalStyles.itemBoxes}>
            content your friends post
            <br/>
            <img class={styles.image_content} src={friend_post}/>
            </li>
          <li class={globalStyles.itemBoxes}>
            your activity on Facebook
            <br/>
            <img class={styles.image_activity} src={activity}/>
          </li>
          <li class={globalStyles.itemBoxes}>
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
