#### Install

```sh
python setup.py install
```

#### Testing

Once installed you can run the program by executing `ae-testing`

Options you can provide to the script. You can always see the help by running
```sh
ae-testing --help
```
Option | Description
--- | ---
**--url** | URL of the AE5 instance you want to run through testing.
*--username* | Username of an administrator to the system. Default is "anaconda-enterprise"
*--password* | Password of an administrator to the system. Default is "anaconda-enterprise"
*--cycles* | Number of cycles to execute. Default is 100.
*--pool-size* | Size of the user pool to use. Default is 20.
*--user-prefix* | The prefix of the user to use. Default is "user".

**Bolded** options are required.

#### Details about Cycles, Pool Size, and Users

###### Cycles
A cycle is defined as creating a project, starting the project session, stopping the session, and removing the project for each user in the pool.

###### Pool Size
The pool size is the number of users to use within a cycle. Default is 20 users but can be changed per your needs.

###### User Prefix
User prefix is the beginning of the username that the script assumes. All users are laid out in the following way.

*USER-PREFIX* + *POOL-NUMBER*

If user-prefix is **user** and pool-size is **20**, then on the system there should be *user01* through *user20* setup and allowed to login and create projects. The password for each of the users would be the same as the username i.e. *user01* would have a password of *user01*.

#### Examples
---
Runs the testing script for one cycle with one user. There would only be a single user *user01* setup on the test system.
```sh
ae-testing --url test.dev.anaconda.com --cycles 1 --pool-size 1
```
---
Runs the testing script for 100 cycles, for 20 users, and the users are setup as *test01* through *test20* with the passwords the same as the username.
```sh
ae-testing --url test.dev.anaconda.com --user-prefix test
```
---
#### Uninstall

```sh
pip uninstall ae-stress
```
