import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageOne.module.css";

const StageOne = (props) => {
  const [url, seturl] = useState([]);
  useEffect(() => {
    const responseUsersShared= fetch("http://127.0.0.1:5000/stage_one_query", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }).then(res => res.json()).then(data => {
      seturl(data);
    });
  }, []);

  return (
    <div className={globalStyles.background}>
      <h1>What have you shared on your profile?</h1>
      <div class={globalStyles.mainContent} >
      <div class={styles.centered}>
      <a href={url} target="_blank" rel="noopener noreferrer">
      {(url.length>1) && (<button class={styles.linktofb}>
        View Your Info on Facebook
      </button>)}
      </a>
      </div>
        <div className={globalStyles.ButtonContainer}>
          <Link to="/StageTwoStepOne">
            <button className={globalStyles.ButtonNav}>
              Next
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default StageOne;
