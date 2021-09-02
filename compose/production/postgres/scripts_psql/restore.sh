#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


# we might run into trouble when using the default `postgres` user, e.g. when dropping the postgres
# database in restore.sh. Check that something else is used here
if [ "$POSTGRES_USER" == "postgres" ]
then
    echo "restoring as the postgres user is not supported, make sure to set the POSTGRES_USER environment variable"
    exit 1
fi

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=$POSTGRES_PASSWORD

# check that we have an argument for a filename candidate
if [[ $# -eq 0 ]] ; then
    echo 'uso:'
    echo '    docker exec -it <nome-container-bd> restore <backup-arquivo>'
    echo ''
    echo 'para obter uma lista dos backups disponíveis, execute:'
    echo '    docker exec -it <nome-container-bd> list-backups'
    exit 1
fi

# set the backupfile variable
BACKUPFILE=/backups/$1

# check that the file exists
if ! [ -f $BACKUPFILE ]; then
    echo "arquivo de backup não encontrado"
    echo 'para obter uma lista dos backups disponíveis, execute:'
    echo '    docker exec -it <nome-container-bd> list-backups'
    exit 1
fi

echo "iniciando restauração de $1"
echo "---------------------------"

# delete the db
# deleting the db can fail. Spit out a comment if this happens but continue since the db
# is created in the next step
echo "deletando o BD antigo $POSTGRES_USER"
if dropdb -h postgres -U $POSTGRES_USER $POSTGRES_USER
then echo "deletado $POSTGRES_USER"
else echo "banco $POSTGRES_USER não existe, continue"
fi

# create a new database
echo "criando novo banco $POSTGRES_USER"
createdb -h postgres -U $POSTGRES_USER $POSTGRES_USER -O $POSTGRES_USER

# restore the database
echo "restaurando banco $POSTGRES_USER"
gunzip -c $BACKUPFILE | psql -h postgres -U $POSTGRES_USER
