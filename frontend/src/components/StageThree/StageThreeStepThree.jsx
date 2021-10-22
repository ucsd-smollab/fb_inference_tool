import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import CategorySelection from "./components/categorySelection";
import globalStyles from "./StageThree.module.css";
import styles from "./StageThreeStepThree.module.css";

const StageThreeStepThree = (props) => {
  const [categories, changeCategories] = useState([]);
  const [friendsDirect, changeFriendsDirect] = useState([]);
  const [friendsInferred, changeFriendsInferred] = useState([]);
  const [categorySelected, changeCategorySelected] = useState(null);

  useEffect(() => {
    // make call to fetch friends
    changeFriendsDirect(["a", "b", "c", "d", "e"]);
    changeFriendsInferred(["z", "y", "x", "w", "v"]);
    changeCategories([
      "friends who have lived in San Diego",
      "friends who have worked at Arby's",
      "friends who attended Camden High",
      "friends who are Catholic",
    ]);
  }, []);

  const selectCateory = (category) => {
    changeCategorySelected(category);
  }

  return (
    <div className={globalStyles.background}>
      <br />
      <br />
      <br />
      <br />
      <div className={globalStyles.CenterTitleContainer}>
        <span className={globalStyles.CenterTitle}>Select a Category</span>
      </div>
      <br />
      <br />
      <br />
      <br />
      <div className={globalStyles.MainBodyContainer}>
        <div className={styles.CategoryListContainer}>
          {categories.map((category) => (
            <CategorySelection category={category} changeCategory={selectCateory} selectedCategory={categorySelected} />
          ))}
        </div>

        <div>
          <div>
            <span>shared directly</span>
          </div>
          <div>
            <span>inferred</span>
          </div>
        </div>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepTwoOne">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
  );
};

export default StageThreeStepThree;
