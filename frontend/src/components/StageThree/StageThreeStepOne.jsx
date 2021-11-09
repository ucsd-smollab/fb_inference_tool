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
      <div className={globalStyles.mainContent}>
      <div className={`${globalStyles.flex_container} ${globalStyles.two_column}`}>
        <span className={`${globalStyles.itemBoxes} ${globalStyles.longBox}`}>
            <h2>Some of your friends have shared a lot:</h2>
          <div>
            {friendsManyShared.map((friend) => <div className={globalStyles.medText}>{friend}</div>)}
          </div>
        </span>
        <span className={`${globalStyles.itemBoxes} ${globalStyles.longBox}`}>
          <h2>Others haven't shared much at all:</h2>
          <div>
            {friendsSparseShared.map((friend) => <div className={globalStyles.medText}>{friend}</div>)}
          </div>
        </span>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepTwoOne">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
    </div>
  );
};

export default StageThreeStepOne;
