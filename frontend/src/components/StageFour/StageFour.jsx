import { useEffect, useState } from "react";

import FriendBox from "./Components/FriendBox";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageFour.modules.css";

const StageFour = (props) => {
  const [query, changeQuery] = useState("");
  const [friendData, changeFriendData] = useState([]);

  useEffect(() => {
    changeFriendData(["gello", "hello", "wow"]);
  }, []);

  return (
    <div className={globalStyles.background}>
      <input className={mainStyles.SearchBar} placeholder="Enter your Friend's Name" onChange={event => changeQuery(event.target.value)} />
      <div className={mainStyles.MainBody}>
        {friendData.filter(friend => {
          if (query === '' || friend.toLowerCase().includes(query.toLowerCase())) {
            return friend;
          }
        }).map( (friend, index) => 
          <FriendBox friend={friend}/>
        )}
      </div>
    </div>
  );
};

export default StageFour;
