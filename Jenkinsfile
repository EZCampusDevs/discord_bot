/*
 * Copyright (C) 2022-2023 EZCampus 
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

pipeline { 
    agent any  

        stages { 

            stage('Build Env File') {

                steps {

                    withCredentials([string(credentialsId: 'DISCORD_BOT_TOKEN', variable: 'DISCORD_TOKEN')]) {

                        writeFile file: './.env', text: """
BOT_TOKEN="${DISCORD_TOKEN}" 
"""
                        }
                }
            }

            stage('Build Docker Image') { 

                steps { 

                    sshPublisher(
                            failOnError: true,
                            publishers: [
                            sshPublisherDesc(
                                configName: '2GB_Glassfish_VPS',
                                transfers: [
                                sshTransfer(cleanRemote: true,
                                    excludes: '',
                                    execCommand: '''
                                    cd ~/pipeline_discord_bot
                                    
                                    log_dir="$HOME/log/jenkins-ssh"
                                    mkdir -p $log_dir
                            
                                    log_file="$log_dir/pipeline_discord_deploy.out"
                                    touch $log_file
                            
                                    exec 3>&1 4>&2
                                    trap 'exec 2>&4 1>&3' 0 1 2 3
                                    exec 1>$log_file 2>&1
                                    

                                    
                                   
                                    docker build -t ezcampus_discord_bot .
                                    rm -f ./.env
                                            
                                            
                                            
                                    is_container_running() {
                                       
                                        container_name="$1"
                                    
                                        if [ "$(docker inspect -f '{{.State.Running}}' "$container_name" 2>/dev/null)" = "true" ]; then
                                    
                                          return 0
                                    
                                       else 
                                    
                                          return 1
                                    
                                       fi
                                    
                                    }
                                        
                                    kill_and_wait_until_container_stopped() {
                                    
                                       container_name="$1"
                                    
                                       while is_container_running $container_name; do
                                    
                                          docker stop "$container_name" || true
                                    
                                          echo "Waiting for container to stop..."
                                    
                                          sleep 1
                                       done
                                    }
                                        
                                    new_container() {
                                    
                                        container="$1"
                                        num="$2"
                                        kill_num="$3"
                                        
                                        
                                        if ! is_container_running "${container}_${num}"; then
                                        
                                            echo "Starting docker container ${num}"

                                            docker run -itd \
                                                --network EZnet \
                                                --name "${container}_${num}" \
                                                ezcampus_discord_bot
                                                
                                            echo "Docker container ${num} started, waiting 15 seconds of grace..."
                                            
                                            sleep 15
                                        
                                            echo "Killing container ${kill_num}"
                                            
                                            kill_and_wait_until_container_stopped "${container}_${kill_num}"
                                            
                                            return 0
                                        
                                        fi
                                        
                                        return 1
                                        
                                    }



                                    container="discord_bot_prod"

                                    if ! new_container "$container" "a" "b"; then
                                    
                                        if ! new_container "$container" "b" "a"; then
                                        
                                            exit 1
                                            
                                        fi
                                    
                                    fi                                   

                                    
                                    ''',
                                    execTimeout: 120000,
                                    flatten: false,
                                    makeEmptyDirs: true, 
                                    noDefaultExcludes: false,
                                    patternSeparator: '[, ]+',
                                    remoteDirectory: 'pipeline_discord_bot',
                                    remoteDirectorySDF: false, 
                                    removePrefix: '', 
                                    sourceFiles: 'Dockerfile, requirements.txt, .env, entrypoint.sh, ezcampus/**/*')
                                ], 
                            usePromotionTimestamp: false,
                            useWorkspaceInPromotion: false,
                            verbose: false)
                                ])
                }
            }
        }

    post {

        always {

            discordSend(
                    description: currentBuild.result, 
                    enableArtifactsList: false, 
                    footer: '', 
                    image: '', 
                    link: '', 
                    result: currentBuild.result, 
                    scmWebUrl: '', 
                    thumbnail: '', 
                    title: env.JOB_BASE_NAME, 
                    webhookURL: "${DISCORD_WEBHOOK_1}"
                    )
        }
    }
}