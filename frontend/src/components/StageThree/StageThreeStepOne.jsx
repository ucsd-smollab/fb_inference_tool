import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageThree.module.css";

const StageThreeStepOne = (props) => {
  const [friendsManyShared, changeFriendsMany] = useState([]);
  const [friendsSparseShared, changeFriendsSparse] = useState([]);

  useEffect(() => {
    // make call to fetch friends
    changeFriendsMany(["a", "b", "c", "d", "e"]);
    changeFriendsSparse(["z", "y", "x", "w", "v"]);
  }, []);

  return (
    <div className={globalStyles.background}>
      <h1>Your Friends</h1>
      <div className={styles.columns_container}>
        <span className={styles.left_column}>
          <h2>Some of your friends have shared a lot:</h2>
          <div>
            {friendsManyShared.map((friend) => <div className={styles.friend_text} >{friend}</div>)}
          </div>
        </span>
        <span className={styles.right_column}>
          <h2>Others haven't shared much at all:</h2>
          <div>
            {friendsSparseShared.map((friend) => <div className={styles.friend_text} >{friend}</div>)}
          </div>
        </span>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepTwoOne">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
  );
};

export default StageThreeStepOne;
