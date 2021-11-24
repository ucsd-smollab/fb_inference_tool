import { useEffect, useState } from "react";

import FriendBox from "./Components/FriendBox";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageFour.modules.css";

const StageFour = (props) => {
  const exampleFriendData = {
    name: 'Jacey Smith',
    mutualFriendCount: '321',
    profilePictureURL: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREQSG0xK1r5xe4WvQsV7WTNey9OSBunMh6GLY8HcxYUinuG_hHJ4IWUtjeAcV3M7bfhbo&usqp=CAU',
    workplace: ['UCSD Department of Computer Science'],
    college: ['University of California San Diego'],
    highschool: ['No Data'],
    places: ['Los Angeles', 'San Diego'],
    religion: ['No Data'],
    politics: ['No Data']
  };

  const [query, changeQuery] = useState("");
  const [selectedFriend, changeSelectedFriend] = useState("aaron.broukhim");
  const [friendData, changeFriendData] = useState(exampleFriendData);
  const [searchFriendSuggestions, changeSearchFriendSuggestions] = useState([]);

  useEffect(() => {
    const request_body = {
      "friend_url": selectedFriend,
    }
    const getFriendData = fetch("http://localhost:5000/stage_four_friend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request_body),
    }).then(res => res.json()).then(data => {
      changeFriendData(data)
    });
  }, [selectedFriend]);

  useEffect(() => {
    const request_body = {
      "query": query,
    }
    const getFriendQuery= fetch("http://localhost:5000/stage_four_query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request_body)
    }).then(res => res.json()).then(data => {
      changeSearchFriendSuggestions(data)
    });
  }, [query]);

  return (
    <div className={globalStyles.background}>
    <div className={globalStyles.SearchContainer}>
      <div className={globalStyles.SearchBar}>
        <input type="text" placeholder="" onChange={event => changeQuery(event.target.value)} />
      </div>
    </div>
    <FriendBox friend={friendData}/>
    </div>
  );
};

export default StageFour;
