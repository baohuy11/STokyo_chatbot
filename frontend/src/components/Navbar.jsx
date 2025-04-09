import {useLocation, useNavigate, Link} from 'react-router-dom'

function NavBar(){
    const navigate = useNavigate();
    const location = useLocation();
    return(
        <div className="navbar bg-base-100 w-[95%]">
            <div className="navbar-start">
                <div className='dropdown'>
                    <label tabIndex={0} className="btn btn-ghost lg:hidden">
                        <svg
                          xmlns="htpp://"
                        >
                            <path/>
                        </svg>
                    </label>
                </div>
            </div>
        </div>
    );
}
export default NavBar;