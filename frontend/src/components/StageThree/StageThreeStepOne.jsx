import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageThree.module.css";

const StageThreeStepOne = (props) => {
  const [friendsManyShared, changeFriendsMany] = useState([]);
  const [friendsSparseShared, changeFriendsSparse] = useState([]);

  useEffect(() => {
    const responseUsersShared= fetch("http://127.0.0.1:5000/stage_three_step_one", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }).then(res => res.json()).then(data => {
      changeFriendsMany(data[1])
      changeFriendsSparse(data[0])
    });
  }, []);

  return (
    <div className={globalStyles.background}>
      <h1>Your Friends</h1>
        <div className={styles.flex_container}>
          <span className={styles.flex_items}>
              <h3 style={{"fontWeight": "bold"}}>Some of your friends have shared a lot:</h3>
            <div>
              {friendsManyShared.map((friend) => <div className={globalStyles.medText}>{friend}</div>)}
            </div>
          </span>
          <span className={styles.flex_items}>
            <h3 style={{"fontWeight": "bold"}}>Others haven't shared much at all:</h3>
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
  );
};

export default StageThreeStepOne;
